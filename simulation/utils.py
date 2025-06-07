from model_parameters import ModelParameters
from numpy import random
from patients.patient import Patient

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