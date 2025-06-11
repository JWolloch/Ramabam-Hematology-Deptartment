from model_parameters import ModelParameters
from numpy import random
from patients.patient import Patient
from patients.leukemia_patient import LeukemiaPatient
from patients.transplant_patient import TransplantPatient
from patients.other_patient import OtherPatient
from simulation.python_sim import SimClasses

def assign_nurse_station(patient_type: str, parameters: ModelParameters) -> str:
    u = random.uniform(0, 1)
    if patient_type == "leukemia":
        p_1 = parameters.nurse_station_1_assignment_probability_leukemia
        p_2 = parameters.nurse_station_2_assignment_probability_leukemia
        p_3 = parameters.nurse_station_3_assignment_probability_leukemia
        p_4 = parameters.nurse_station_4_assignment_probability_leukemia
        p_5 = parameters.nurse_station_5_assignment_probability_leukemia
        if u < p_1:
            return "nurse_station_1"
        elif u < p_1 + p_2:
            return "nurse_station_2"
        elif u < p_1 + p_2 + p_3:
            return "nurse_station_3"
        elif u < p_1 + p_2 + p_3 + p_4:
            return "nurse_station_4"
        elif u < p_1 + p_2 + p_3 + p_4 + p_5:
            return "nurse_station_5"
        else:
            raise ValueError("Issue with Leukemia nurse assignment probabilities")
        
    elif patient_type == "transplant":
        p_1 = parameters.nurse_station_1_assignment_probability_transplant
        p_2 = parameters.nurse_station_2_assignment_probability_transplant
        p_3 = parameters.nurse_station_3_assignment_probability_transplant
        p_4 = parameters.nurse_station_4_assignment_probability_transplant
        p_5 = parameters.nurse_station_5_assignment_probability_transplant
        if u < p_1:
            return "nurse_station_1"
        elif u < p_1 + p_2:
            return "nurse_station_2"
        elif u < p_1 + p_2 + p_3:
            return "nurse_station_3"
        elif u < p_1 + p_2 + p_3 + p_4:
            return "nurse_station_4"
        elif u < p_1 + p_2 + p_3 + p_4 + p_5:
            return "nurse_station_5"
        else:
            return "nurse_station_6"
        
    elif patient_type == "other":
        p_1 = parameters.nurse_station_1_assignment_probability_other
        p_2 = parameters.nurse_station_2_assignment_probability_other
        p_3 = parameters.nurse_station_3_assignment_probability_other
        p_4 = parameters.nurse_station_4_assignment_probability_other
        p_5 = parameters.nurse_station_5_assignment_probability_other
        if u < p_1:
            return "nurse_station_1"
        elif u < p_1 + p_2:
            return "nurse_station_2"
        elif u < p_1 + p_2 + p_3:
            return "nurse_station_3"
        elif u < p_1 + p_2 + p_3 + p_4:
            return "nurse_station_4"
        elif u < p_1 + p_2 + p_3 + p_4 + p_5:
            return "nurse_station_5"
        else:
            raise ValueError("Issue with Other nurse assignment probabilities")

def all_left_department(patients: list[list[Patient]]) -> bool:
    for patient_list in patients:
        for patient in patient_list:
            if not patient.left_department:
                return False
    return True

def create_patient_schedule(arrival_time: int):
    return {'arrival_time': arrival_time,
            'doctor_consultation_time': arrival_time + 120}

def initialize_patients(patient_arrival_times: list[int],
                        doctor_name: str,
                        calendar: SimClasses.EventCalendar,
                        model_parameters: ModelParameters):
    leukemia = 'leukemia' in doctor_name
    transplant = 'transplant' in doctor_name
    patients = []
    if leukemia:
        probability_of_visiting_nurse = model_parameters.probability_of_visiting_nurse_leukemia

        if '1' in doctor_name:
            probability_of_complex_patient = model_parameters.leukemia_doctor_1_probability_of_complex_patient
        else:
            probability_of_complex_patient = model_parameters.leukemia_doctor_2_probability_of_complex_patient

        for arrival_time in patient_arrival_times:
            patients.append(LeukemiaPatient(create_patient_schedule(arrival_time),
                                            doctor_name,
                                            probability_of_complex_patient,
                                            probability_of_visiting_nurse))
    elif transplant:
        probability_of_visiting_nurse = model_parameters.probability_of_visiting_nurse_transplant
        if '1' in doctor_name:
            probability_of_complex_patient = model_parameters.transplant_doctor_1_probability_of_complex_patient
        elif '2' in doctor_name:
            probability_of_complex_patient = model_parameters.transplant_doctor_2_probability_of_complex_patient
        else:
            probability_of_complex_patient = model_parameters.transplant_doctor_3_probability_of_complex_patient

        for arrival_time in patient_arrival_times:
            patients.append(TransplantPatient(create_patient_schedule(arrival_time),
                                              doctor_name,
                                              probability_of_complex_patient,
                                              probability_of_visiting_nurse))
    else: #other
        probability_of_visiting_nurse = model_parameters.probability_of_visiting_nurse_other
        probability_of_complex_patient = model_parameters.probability_of_complex_other_patient

        for arrival_time in patient_arrival_times:
            patients.append(OtherPatient(create_patient_schedule(arrival_time),
                                         doctor_name,
                                         probability_of_complex_patient,
                                         probability_of_visiting_nurse))
    
    for patient in patients:
        patient.schedule_arrival(calendar)
        
    return patients

def generate_patients(calendar: SimClasses.EventCalendar,parameters: ModelParameters):
    
    leukemia_doctor_1_number_of_patients = parameters.leukemia_doctor_1_number_of_regular_patients + parameters.leukemia_doctor_1_number_of_complex_patients
    leukemia_doctor_1_patient_arrival_times = [60 + i*20 for i in range(leukemia_doctor_1_number_of_patients)]
    leukemia_doctor_2_number_of_patients = parameters.leukemia_doctor_2_number_of_regular_patients + parameters.leukemia_doctor_2_number_of_complex_patients
    leukemia_doctor_2_patient_arrival_times = [60 + i*20 for i in range(leukemia_doctor_2_number_of_patients)]

    transplant_doctor_1_number_of_patients = parameters.transplant_doctor_1_number_of_regular_patients + parameters.transplant_doctor_1_number_of_complex_patients
    transplant_doctor_1_patient_arrival_times = [60 + i*20 for i in range(transplant_doctor_1_number_of_patients)]
    transplant_doctor_2_number_of_patients = parameters.transplant_doctor_2_number_of_regular_patients + parameters.transplant_doctor_2_number_of_complex_patients
    transplant_doctor_2_patient_arrival_times = [60 + i*20 for i in range(transplant_doctor_2_number_of_patients)]
    transplant_doctor_3_number_of_patients = parameters.transplant_doctor_3_number_of_regular_patients + parameters.transplant_doctor_3_number_of_complex_patients
    transplant_doctor_3_patient_arrival_times = [60 + i*20 for i in range(transplant_doctor_3_number_of_patients)]

    other_patients_arrival_times = [60 + i*10 for i in range(parameters.number_of_other_patients)]

    leukemia_doctor_1_patients = initialize_patients(leukemia_doctor_1_patient_arrival_times, "leukemia_doctor_1", calendar, parameters)
    leukemia_doctor_2_patients = initialize_patients(leukemia_doctor_2_patient_arrival_times, "leukemia_doctor_2", calendar, parameters)
    transplant_doctor_1_patients = initialize_patients(transplant_doctor_1_patient_arrival_times, "transplant_doctor_1", calendar, parameters)
    transplant_doctor_2_patients = initialize_patients(transplant_doctor_2_patient_arrival_times, "transplant_doctor_2", calendar, parameters)
    transplant_doctor_3_patients = initialize_patients(transplant_doctor_3_patient_arrival_times, "transplant_doctor_3", calendar, parameters)
    other_patients = initialize_patients(other_patients_arrival_times, "other", calendar, parameters)
    list_of_patients = [leukemia_doctor_1_patients, leukemia_doctor_2_patients, transplant_doctor_1_patients, transplant_doctor_2_patients, transplant_doctor_3_patients, other_patients]

    return list_of_patients