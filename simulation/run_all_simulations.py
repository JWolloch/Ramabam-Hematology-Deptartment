import subprocess
import sys
import os
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'simulation_configuration.py')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'output.txt')

# Helper to change personalize_schedule in the config file
def set_personalize_schedule(value: bool):
    with open(CONFIG_FILE, 'r') as f:
        lines = f.readlines()
    with open(CONFIG_FILE, 'w') as f:
        for line in lines:
            if line.strip().startswith('personalize_schedule: bool ='):
                f.write(f'    personalize_schedule: bool = {str(value)}\n')
            else:
                f.write(line)

def run_script(script_path, output_file):
    message = f'Running {script_path}...'
    print(message)
    output_file.write(message + '\n')
    output_file.flush()
    
    # Set environment variables to prevent output truncation
    env = os.environ.copy()
    env.update({
        'PYTHONUNBUFFERED': '1',  # Prevent Python output buffering
        'PANDAS_OPTIONS_DISPLAY_MAX_ROWS': '1000',  # Increase max rows displayed
        'PANDAS_OPTIONS_DISPLAY_MAX_COLUMNS': '1000',  # Increase max columns displayed
        'PANDAS_OPTIONS_DISPLAY_WIDTH': '1000',  # Increase display width
        'PANDAS_OPTIONS_DISPLAY_MAX_COLWIDTH': '1000',  # Increase max column width
    })
    
    result = subprocess.run(
        [sys.executable, '-c', 
         'import pandas as pd; '
         'pd.set_option("display.max_rows", None); '
         'pd.set_option("display.max_columns", None); '
         'pd.set_option("display.width", None); '
         'pd.set_option("display.max_colwidth", None); '
         f'exec(open("{script_path}").read())'],
        capture_output=True, 
        text=True, 
        env=env
    )
    
    # Write stdout to file
    if result.stdout:
        print(result.stdout)
        output_file.write(result.stdout)
        output_file.flush()
    
    # Write stderr to file if there are errors
    if result.returncode != 0:
        print(result.stderr)
        output_file.write(result.stderr)
        output_file.flush()
        raise RuntimeError(f"Script {script_path} failed.")

if __name__ == '__main__':
    # Open output file for writing
    with open(OUTPUT_FILE, 'w') as output_file:
        # Write timestamp header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"=== Simulation Run Started at {timestamp} ===\n\n"
        print(header.strip())
        output_file.write(header)
        output_file.flush()
        
        # Save original config
        with open(CONFIG_FILE, 'r') as f:
            original_config = f.read()
        try:
            for personalize in [False, True]:
                set_personalize_schedule(personalize)
                section_header = f"\n=== Running with personalize_schedule = {personalize} ===\n"
                print(section_header.strip())
                output_file.write(section_header)
                output_file.flush()
                
                run_script(os.path.join(os.path.dirname(__file__), 'multi_queue_simulation.py'), output_file)
                run_script(os.path.join(os.path.dirname(__file__), 'single_queue_simulation.py'), output_file)
        finally:
            # Restore original config
            with open(CONFIG_FILE, 'w') as f:
                f.write(original_config)
            
            restore_message = "\nRestored original simulation_configuration.py."
            print(restore_message)
            output_file.write(restore_message + '\n')
            output_file.flush()
            
            completion_message = f"\n=== Simulation Run Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==="
            print(completion_message)
            output_file.write(completion_message + '\n')
            
    print(f"\nAll outputs have been written to {OUTPUT_FILE}") 