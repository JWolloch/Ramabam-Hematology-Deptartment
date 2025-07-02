import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any
from model_parameters import ModelParametersMultiQueue
import utils as utils

class PatientProfileGenerator:
    def __init__(self, num_profiles=100, seed=42):
        self.num_profiles = num_profiles
        self.seed = seed
        self.parameters = ModelParametersMultiQueue()
        self.profiles = []
        
    def generate_patient_profile(self, profile_id: int) -> Dict[str, Any]:
        """Generate a single patient profile with all necessary information"""
        # Set seed for reproducibility
        np.random.seed(self.seed + profile_id)
        
        profile = {
            'profile_id': profile_id,
            'patient_counts': {},
            'patient_details': {}
        }
        
        # Generate patient counts for each doctor
        profile['patient_counts'] = {
            'leukemia_doctor_1': utils.randomize_number_of_patients(
                self.parameters.leukemia_doctor_1_number_of_patients
            ),
            'leukemia_doctor_2': utils.randomize_number_of_patients(
                self.parameters.leukemia_doctor_2_number_of_patients
            ),
            'transplant_doctor_1': utils.randomize_number_of_patients(
                self.parameters.transplant_doctor_1_number_of_patients
            ),
            'transplant_doctor_2': utils.randomize_number_of_patients(
                self.parameters.transplant_doctor_2_number_of_patients
            ),
            'transplant_doctor_3': utils.randomize_number_of_patients(
                self.parameters.transplant_doctor_3_number_of_patients
            ),
            'other_patients': self.parameters.number_of_other_patients
        }
        
        # Generate detailed patient information for each doctor
        for doctor_name, patient_count in profile['patient_counts'].items():
            if doctor_name == 'other_patients':
                profile['patient_details'][doctor_name] = self._generate_other_patients(patient_count)
            else:
                profile['patient_details'][doctor_name] = self._generate_doctor_patients(
                    doctor_name, patient_count
                )
        
        return profile
    
    def _generate_other_patients(self, count: int) -> List[Dict]:
        """Generate other patients with their attributes"""
        patients = []
        arrival_times = utils.layered_patient_arrival_schedule(count)
        
        for i, arrival_time in enumerate(arrival_times):
            # Generate patient complexity
            is_complex = np.random.random() < self.parameters.probability_of_complex_other_patient
            
            # Generate nurse visit decision
            visits_nurse = np.random.random() < self.parameters.probability_of_visiting_nurse_other
            
            # Generate blood test decision
            needs_long_blood_test = np.random.random() < self.parameters.probability_of_needing_long_blood_test
            
            patient = {
                'patient_id': f'other_{i}',
                'arrival_time': arrival_time,
                'patient_type': 'other',
                'complexity': 'complex' if is_complex else 'regular',
                'visits_nurse': visits_nurse,
                'needs_long_blood_test': needs_long_blood_test,
                'doctor_name': 'other_doctor'
            }
            patients.append(patient)
        
        return patients
    
    def _generate_doctor_patients(self, doctor_name: str, count: int) -> List[Dict]:
        """Generate patients for a specific doctor"""
        patients = []
        arrival_times = utils.layered_patient_arrival_schedule(count)
        
        # Get doctor-specific parameters
        if 'leukemia' in doctor_name:
            if '1' in doctor_name:
                complexity_prob = self.parameters.leukemia_doctor_1_probability_of_complex_patient
            else:
                complexity_prob = self.parameters.leukemia_doctor_2_probability_of_complex_patient
            nurse_prob = self.parameters.probability_of_visiting_nurse_leukemia
        elif 'transplant' in doctor_name:
            if '1' in doctor_name:
                complexity_prob = self.parameters.transplant_doctor_1_probability_of_complex_patient
            elif '2' in doctor_name:
                complexity_prob = self.parameters.transplant_doctor_2_probability_of_complex_patient
            else:
                complexity_prob = self.parameters.transplant_doctor_3_probability_of_complex_patient
            nurse_prob = self.parameters.probability_of_visiting_nurse_transplant
        
        for i, arrival_time in enumerate(arrival_times):
            # Generate patient complexity
            is_complex = np.random.random() < complexity_prob
            
            # Generate nurse visit decision
            visits_nurse = np.random.random() < nurse_prob
            
            # Generate blood test decision
            needs_long_blood_test = np.random.random() < self.parameters.probability_of_needing_long_blood_test
            
            patient = {
                'patient_id': f'{doctor_name}_{i}',
                'arrival_time': arrival_time,
                'patient_type': 'leukemia' if 'leukemia' in doctor_name else 'transplant',
                'complexity': 'complex' if is_complex else 'regular',
                'visits_nurse': visits_nurse,
                'needs_long_blood_test': needs_long_blood_test,
                'doctor_name': doctor_name
            }
            patients.append(patient)
        
        return patients
    
    def generate_all_profiles(self) -> List[Dict]:
        """Generate all patient profiles"""
        print(f"Generating {self.num_profiles} patient profiles...")
        
        for i in range(self.num_profiles):
            profile = self.generate_patient_profile(i)
            self.profiles.append(profile)
        
        print(f"Generated {len(self.profiles)} patient profiles")
        return self.profiles
    
    def save_profiles(self, filename: str = 'cached_patient_profiles.json'):
        """Save profiles to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.profiles, f, indent=2)
        print(f"Saved {len(self.profiles)} profiles to {filename}")
    
    def load_profiles(self, filename: str = 'cached_patient_profiles.json') -> List[Dict]:
        """Load profiles from JSON file"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.profiles = json.load(f)
            print(f"Loaded {len(self.profiles)} profiles from {filename}")
            return self.profiles
        else:
            print(f"Profile file {filename} not found. Generating new profiles...")
            return self.generate_all_profiles()
    
    def get_profile(self, profile_id: int) -> Dict:
        """Get a specific profile by ID"""
        if profile_id < len(self.profiles):
            return self.profiles[profile_id]
        else:
            raise ValueError(f"Profile ID {profile_id} not found. Only {len(self.profiles)} profiles available.")
    
    def export_to_csv(self, filename: str = 'patient_profiles.csv'):
        """Export profiles to CSV for easy inspection"""
        rows = []
        
        for profile in self.profiles:
            profile_id = profile['profile_id']
            
            for doctor_name, patients in profile['patient_details'].items():
                for patient in patients:
                    row = {
                        'profile_id': profile_id,
                        'doctor_name': doctor_name,
                        'patient_id': patient['patient_id'],
                        'arrival_time': patient['arrival_time'],
                        'patient_type': patient['patient_type'],
                        'complexity': patient['complexity'],
                        'visits_nurse': patient['visits_nurse'],
                        'needs_long_blood_test': patient['needs_long_blood_test']
                    }
                    rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(filename, index=False)
        print(f"Exported profiles to {filename}")
        return df
    
    def print_profile_summary(self, profile_id: int = None):
        """Print summary of profiles"""
        if profile_id is not None:
            profile = self.get_profile(profile_id)
            print(f"\nProfile {profile_id} Summary:")
            print(f"Total patients: {sum(profile['patient_counts'].values())}")
            for doctor, count in profile['patient_counts'].items():
                print(f"  {doctor}: {count} patients")
        else:
            print(f"\nAll Profiles Summary:")
            print(f"Total profiles: {len(self.profiles)}")
            
            # Calculate average patient counts
            avg_counts = {}
            for profile in self.profiles:
                for doctor, count in profile['patient_counts'].items():
                    if doctor not in avg_counts:
                        avg_counts[doctor] = []
                    avg_counts[doctor].append(count)
            
            for doctor, counts in avg_counts.items():
                print(f"  {doctor}: {np.mean(counts):.1f} ± {np.std(counts):.1f} patients")

def main():
    """Main function to generate and cache patient profiles"""
    # Create generator
    generator = PatientProfileGenerator(num_profiles=100, seed=42)
    
    # Generate profiles
    profiles = generator.generate_all_profiles()
    
    # Save to file
    generator.save_profiles()
    
    # Export to CSV for inspection
    generator.export_to_csv()
    
    # Print summary
    generator.print_profile_summary()
    
    # Print detailed summary of first profile
    generator.print_profile_summary(0)
    
    return generator

if __name__ == "__main__":
    main() 