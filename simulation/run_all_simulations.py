import subprocess
import sys
import os

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

def run_script(script_path):
    print(f'Running {script_path}...')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Script {script_path} failed.")

if __name__ == '__main__':
    # Save original config
    with open(CONFIG_FILE, 'r') as f:
        original_config = f.read()
    try:
        for personalize in [False, True]:
            set_personalize_schedule(personalize)
            print(f"\n=== Running with personalize_schedule = {personalize} ===\n")
            run_script(os.path.join(os.path.dirname(__file__), 'multi_queue_simulation.py'))
            run_script(os.path.join(os.path.dirname(__file__), 'single_queue_simulation.py'))
    finally:
        # Restore original config
        with open(CONFIG_FILE, 'w') as f:
            f.write(original_config)
        print("\nRestored original simulation_configuration.py.") 