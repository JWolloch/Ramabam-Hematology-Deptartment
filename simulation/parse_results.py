import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.table import Table

def parse_simulation_output(file_path):
    """
    Parse the simulation output file and extract statistical metrics.
    Returns a list of dictionaries with metric data.
    """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse means and confidence intervals
    metrics_data = []
    
    # Find all "Means of the simulation results:" sections
    means_pattern = r'Means of the simulation results:\n(.*?)\n\*+'
    ci_pattern = r'99% Confidence Intervals Half-Width\n(.*?)\n\*+'
    
    means_matches = re.findall(means_pattern, content, re.DOTALL)
    ci_matches = re.findall(ci_pattern, content, re.DOTALL)
    
    # Track which section we're in
    section_markers = re.findall(r'=== Running with personalize_schedule = (False|True) ===', content)
    simulation_markers = re.findall(r'Running .*(multi_queue|single_queue)_simulation\.py', content)
    
    # Process each means section with its corresponding CI section
    for i, (means_text, ci_text) in enumerate(zip(means_matches, ci_matches)):
        # Determine section type
        section_idx = i // 2  # Two simulations per section
        sim_idx = i % 2       # 0 for multi_queue, 1 for single_queue
        
        if section_idx < len(section_markers):
            section_type = "current_state" if section_markers[section_idx] == "False" else "personalized"
        else:
            section_type = "unknown"
            
        simulation_type = "multi_queue" if sim_idx == 0 else "single_queue"
        
        # Parse means
        means_lines = means_text.strip().split('\n')
        ci_lines = ci_text.strip().split('\n')
        
        # Create dictionaries for quick lookup
        means_dict = {}
        ci_dict = {}
        
        for line in means_lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                metric_name = parts[0]
                # Skip variance-related metrics
                if '_var' in metric_name or 'variance' in metric_name.lower():
                    continue
                try:
                    value = float(parts[1])
                    means_dict[metric_name] = value
                except ValueError:
                    continue
        
        for line in ci_lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                metric_name = parts[0]
                # Skip variance-related metrics
                if '_var' in metric_name or 'variance' in metric_name.lower():
                    continue
                try:
                    ci_half_width = float(parts[1])
                    ci_dict[metric_name] = ci_half_width
                except ValueError:
                    continue
        
        # Combine means and CIs
        for metric_name, mean_value in means_dict.items():
            ci_half_width = ci_dict.get(metric_name, abs(mean_value) * 0.05)  # Default 5% if not found
            
            metrics_data.append({
                'section': section_type,
                'simulation_type': simulation_type,
                'metric': metric_name,
                'mean': mean_value,
                'ci_lower': mean_value - ci_half_width,
                'ci_upper': mean_value + ci_half_width,
                'ci_half_width': ci_half_width
            })
    
    return metrics_data

def create_individual_table_png(section_data, filename, title):
    """
    Create a visual table for a specific simulation configuration.
    """
    if not section_data:
        print(f"No data for {title}")
        return
    
    # Calculate figure size based on number of rows
    n_rows = len(section_data)
    fig_height = max(12, n_rows * 0.35 + 4)
    fig_width = 16  # Even wider to accommodate long metric names on single lines
    
    fig, ax = plt.subplots(1, 1, figsize=(fig_width, fig_height))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = []
    headers = ['Metric', 'Mean', 'CI Lower Bound', 'CI Upper Bound']
    
    for item in section_data:
        # Clean up metric name for display - keep on single line
        clean_metric = item['metric'].replace('_avg', '').replace('_', ' ')
        
        # More intelligent abbreviation for very long names
        if len(clean_metric) > 50:
            # Abbreviate common long words
            clean_metric = clean_metric.replace('Patients Total Processing Time', 'Processing Time')
            clean_metric = clean_metric.replace('Scheduled Vs Actual Time Diff', 'Schedule Difference')
            clean_metric = clean_metric.replace('Station', 'Stn')
            clean_metric = clean_metric.replace('Doctor', 'Dr')
        
        # Capitalize properly
        clean_metric = clean_metric.title()
        
        table_data.append([
            clean_metric,
            f"{item['mean']:.6f}",
            f"{item['ci_lower']:.6f}",
            f"{item['ci_upper']:.6f}"
        ])
    
    # Sort by metric name for consistency
    table_data.sort(key=lambda x: x[0])
    
    # Create table with custom column widths
    table = ax.table(cellText=table_data,
                    colLabels=headers,
                    cellLoc='left',  # Left align for better readability
                    loc='center',
                    bbox=[0, 0, 1, 1])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)  # Reasonable row height
    
    # Set column widths - optimized proportions
    cellDict = table.get_celld()
    for i in range(len(table_data) + 1):  # +1 for header
        # Metric column (wider but not too wide)
        cellDict[(i, 0)].set_width(0.55)
        # Data columns (equal width)
        cellDict[(i, 1)].set_width(0.15)
        cellDict[(i, 2)].set_width(0.15)
        cellDict[(i, 3)].set_width(0.15)
    
    # Style header row
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#2E7D32')
        table[(0, i)].set_text_props(weight='bold', color='white', fontsize=10)
        
    # Alternate row colors and style
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f8f9fa')
            else:
                table[(i, j)].set_facecolor('#ffffff')
            
            # Style based on column
            if j == 0:
                # Metric names: bold and left-aligned
                table[(i, j)].set_text_props(weight='bold', ha='left', fontsize=8)
            else:
                # Numeric data: center-aligned
                table[(i, j)].set_text_props(ha='center', fontsize=9)
    
    # Add title
    plt.suptitle(f'{title}\nTotal metrics: {len(table_data)}', 
                fontsize=18, fontweight='bold', y=0.96)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig(filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"Results table saved as {filename}")

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_txt_path = os.path.join(script_dir, 'output.txt')
    
    print("Parsing simulation output...")
    metrics_data = parse_simulation_output(output_txt_path)
    
    if not metrics_data:
        print("No valid metrics found in output.txt")
        print("Make sure the simulation has been run and output.txt contains results.")
        return
    
    print(f"Found {len(metrics_data)} metrics.")
    
    # Group by section and simulation type
    configurations = {}
    for item in metrics_data:
        config_key = f"{item['simulation_type']}_{item['section']}"
        if config_key not in configurations:
            configurations[config_key] = []
        configurations[config_key].append(item)
    
    # Create separate PNG files for each configuration
    for config_name, config_data in configurations.items():
        filename = os.path.join(script_dir, f'{config_name}_results.png')
        
        # Create title based on configuration
        parts = config_name.split('_')
        sim_type = parts[0].replace('_', ' ').title()
        section_type = parts[1].replace('_', ' ').title()
        title = f'{sim_type} Simulation - {section_type} Configuration'
        
        create_individual_table_png(config_data, filename, title)
    
    print(f"\nCreated {len(configurations)} result files:")
    for config_name in configurations.keys():
        print(f"  - {config_name}_results.png")

if __name__ == '__main__':
    main() 