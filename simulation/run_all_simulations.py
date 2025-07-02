import subprocess
import sys
import os
from tabulate import tabulate

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'simulation_configuration.py')

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

def run_script(script_path, parameters=None):
    print(f'Running {script_path}...')
    if parameters:
        print(f'With custom parameters: {len(parameters)} parameters provided')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Script {script_path} failed.")

def display_parameters_table(multi_queue_params=None, single_queue_params=None):
    """Display parameters in a nice table format"""
    print("\n" + "="*80)
    print("SIMULATION PARAMETERS")
    print("="*80)
    
    if multi_queue_params:
        print("\nMulti-Queue Simulation Parameters:")
        print("-" * 50)
        multi_queue_table = [[key, value] for key, value in multi_queue_params.items()]
        print(tabulate(multi_queue_table, headers=['Parameter', 'Value'], tablefmt='grid'))
    
    if single_queue_params:
        print("\nSingle-Queue Simulation Parameters:")
        print("-" * 50)
        single_queue_table = [[key, value] for key, value in single_queue_params.items()]
        print(tabulate(single_queue_table, headers=['Parameter', 'Value'], tablefmt='grid'))
    
    if not multi_queue_params and not single_queue_params:
        print("Using default parameters for both simulations")
    
    print("="*80 + "\n")

def run_all_simulations(multi_queue_params=None, single_queue_params=None):
    """Run all simulations with optional custom parameters"""
    
    # Display parameters table
    display_parameters_table(multi_queue_params, single_queue_params)
    
    # Save original config
    with open(CONFIG_FILE, 'r') as f:
        original_config = f.read()
    
    try:
        for personalize in [False, True]:
            set_personalize_schedule(personalize)
            print(f"\n=== Running with personalize_schedule = {personalize} ===\n")
            
            # Run multi-queue simulation with custom parameters
            if multi_queue_params:
                # Import and run with parameters
                from multi_queue_simulation import run_multi_queue_simulation
                run_multi_queue_simulation(multi_queue_params)
            else:
                run_script(os.path.join(os.path.dirname(__file__), 'multi_queue_simulation.py'))
            
            # Run single-queue simulation with custom parameters
            if single_queue_params:
                # Import and run with parameters
                from single_queue_simulation import run_single_queue_simulation
                run_single_queue_simulation(single_queue_params)
            else:
                run_script(os.path.join(os.path.dirname(__file__), 'single_queue_simulation.py'))
                
    finally:
        # Restore original config
        with open(CONFIG_FILE, 'w') as f:
            f.write(original_config)
        print("\nRestored original simulation_configuration.py.")

if __name__ == '__main__':
    # Example usage with custom parameters
    # multi_queue_params = {
    #     'leukemia_doctor_1_mean_service_time_regular': 20,
    #     'leukemia_doctor_1_mean_service_time_complex': 25,
    #     # ... add more parameters as needed
    # }
    # single_queue_params = {
    #     'leukemia_doctor_1_mean_service_time_regular': 18,
    #     'leukemia_doctor_1_mean_service_time_complex': 22,
    #     # ... add more parameters as needed
    # }
    
    # For now, run with default parameters
    run_all_simulations() 