from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys
import json
import pandas as pd
from run_all_simulations import run_all_simulations
from model_parameters import ModelParametersMultiQueue, ModelParametersSingleQueue

app = Flask(__name__)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define paths to results directories
RESULTS_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results_directory')
RESULTS_PATHS = {
    'single_queue': {
        'current': os.path.join(RESULTS_BASE_DIR, 'single_queue_v2', 'current_state'),
        'personalized': os.path.join(RESULTS_BASE_DIR, 'single_queue_v2', 'personalized')
    },
    'multi_queue': {
        'current': os.path.join(RESULTS_BASE_DIR, 'multi_queue_v2', 'current_state'),
        'personalized': os.path.join(RESULTS_BASE_DIR, 'multi_queue_v2', 'personalized')
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_default_params')
def get_default_params():
    multi_queue_params = ModelParametersMultiQueue()
    single_queue_params = ModelParametersSingleQueue()
    
    return jsonify({
        'multi_queue': multi_queue_params.__dict__,
        'single_queue': single_queue_params.__dict__
    })

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    try:
        # Add logging for request content type and data
        print("Content-Type:", request.content_type)
        print("Raw Data:", request.get_data())
        
        # Handle both JSON and form data
        if request.content_type and 'application/json' in request.content_type:
            data = request.get_json(force=True)
        else:
            # Handle form data
            data = {
                'multi_queue_params': {},
                'single_queue_params': {}
            }
            for key, value in request.form.items():
                if key.startswith('multi_queue_'):
                    data['multi_queue_params'][key.replace('multi_queue_', '')] = value
                elif key.startswith('single_queue_'):
                    data['single_queue_params'][key.replace('single_queue_', '')] = value
        
        # Convert parameters to float/int where needed
        multi_queue_params = {}
        single_queue_params = {}
        
        if data.get('multi_queue_params'):
            for key, value in data['multi_queue_params'].items():
                try:
                    if isinstance(value, str):
                        if '.' in value:
                            multi_queue_params[key] = float(value)
                        else:
                            multi_queue_params[key] = int(value)
                    else:
                        multi_queue_params[key] = value
                except ValueError as e:
                    print(f"Error converting {key}: {value} - {str(e)}")
                    multi_queue_params[key] = value
        
        if data.get('single_queue_params'):
            for key, value in data['single_queue_params'].items():
                try:
                    if isinstance(value, str):
                        if '.' in value:
                            single_queue_params[key] = float(value)
                        else:
                            single_queue_params[key] = int(value)
                    else:
                        single_queue_params[key] = value
                except ValueError as e:
                    print(f"Error converting {key}: {value} - {str(e)}")
                    single_queue_params[key] = value
        
        # Run simulations
        run_all_simulations(multi_queue_params, single_queue_params)
        
        return jsonify({
            'status': 'success',
            'message': 'Simulations completed successfully',
            'redirect': url_for('results', queue_type='multi_queue', schedule_type='current')
        })
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Error details:", error_details)
        return jsonify({
            'status': 'error',
            'message': f'Error running simulations: {str(e)}',
            'details': error_details
        }), 500

@app.route('/results')
def results():
    queue_type = request.args.get('queue_type', 'multi_queue')
    schedule_type = request.args.get('schedule_type', 'current')
    
    # Load data from CSV files
    try:
        base_path = RESULTS_PATHS[queue_type][schedule_type]
        
        averages_df = pd.read_csv(os.path.join(base_path, 'averages_data.csv'))
        variances_df = pd.read_csv(os.path.join(base_path, 'variances_data.csv'))
        patient_attributes_df = pd.read_csv(os.path.join(base_path, 'patient_attributes.csv'))
        
        # Convert DataFrames to HTML tables with styling
        averages_table = averages_df.to_html(classes=['table', 'table-striped', 'table-hover'], index=False)
        variances_table = variances_df.to_html(classes=['table', 'table-striped', 'table-hover'], index=False)
        patient_attributes_table = patient_attributes_df.to_html(classes=['table', 'table-striped', 'table-hover'], index=False)
        
        return render_template('results.html',
                             queue_type=queue_type,
                             schedule_type=schedule_type,
                             averages_table=averages_table,
                             variances_table=variances_table,
                             patient_attributes_table=patient_attributes_table)
    
    except Exception as e:
        return f"Error loading results: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 