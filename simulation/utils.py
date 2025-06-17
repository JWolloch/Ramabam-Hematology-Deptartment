from model_parameters import ModelParametersMultiQueue, ModelParametersSingleQueue
import numpy as np
import numpy.random as random
from patients.patient import Patient
from patients.leukemia_patient import LeukemiaPatient
from patients.transplant_patient import TransplantPatient
from patients.other_patient import OtherPatient
from python_sim import SimClasses
from python_sim import SimFunctions
import pandas as pd
import os

def assign_nurse_station_multi_queue(patient_type: str, patient_complexity: str, parameters: ModelParametersMultiQueue) -> str:
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
        elif u <= p_1 + p_2 + p_3 + p_4 + p_5:
            return "nurse_station_5"
        else:
            raise ValueError("Issue with Leukemia nurse assignment probabilities")
        
    elif patient_type == "transplant":
        if patient_complexity == "regular":
            p_1 = parameters.nurse_station_1_assignment_probability_transplant_regular
            p_2 = parameters.nurse_station_2_assignment_probability_transplant_regular
            p_3 = parameters.nurse_station_3_assignment_probability_transplant_regular
            p_4 = parameters.nurse_station_4_assignment_probability_transplant_regular
            p_5 = parameters.nurse_station_5_assignment_probability_transplant_regular
            if u < p_1:
                return "nurse_station_1"
            elif u < p_1 + p_2:
                return "nurse_station_2"
            elif u < p_1 + p_2 + p_3:
                return "nurse_station_3"
            elif u < p_1 + p_2 + p_3 + p_4:
                return "nurse_station_4"
            elif u <= p_1 + p_2 + p_3 + p_4 + p_5:
                return "nurse_station_5"
            else:
                return "nurse_station_6"
        
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
        elif u <= p_1 + p_2 + p_3 + p_4 + p_5:
            return "nurse_station_5"
        else:
            raise ValueError("Issue with Other nurse assignment probabilities")

def randomize_number_of_patients(number_of_patients: int) -> int:
    u = random.uniform(0, 1)
    if u < 0.1:
        return number_of_patients - 2
    elif u < 0.25:
        return number_of_patients - 1
    elif u < 0.75:
        return number_of_patients
    elif u < 0.9:
        return number_of_patients + 1
    else:
        return number_of_patients + 2

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
                        model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):
    leukemia = 'leukemia' in doctor_name
    transplant = 'transplant' in doctor_name
    patients = []
    if leukemia:
        probability_of_visiting_nurse = model_parameters.probability_of_visiting_nurse_leukemia
        probability_of_needing_long_blood_test = model_parameters.probability_of_needing_long_blood_test

        if '1' in doctor_name:
            probability_of_complex_patient = model_parameters.leukemia_doctor_1_probability_of_complex_patient
        else:
            probability_of_complex_patient = model_parameters.leukemia_doctor_2_probability_of_complex_patient

        for arrival_time in patient_arrival_times:
            patients.append(LeukemiaPatient(create_patient_schedule(arrival_time),
                                            doctor_name,
                                            probability_of_complex_patient,
                                            probability_of_visiting_nurse,
                                            probability_of_needing_long_blood_test))
    elif transplant:
        probability_of_visiting_nurse = model_parameters.probability_of_visiting_nurse_transplant
        probability_of_needing_long_blood_test = model_parameters.probability_of_needing_long_blood_test

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
                                              probability_of_visiting_nurse,
                                              probability_of_needing_long_blood_test))
    else: #other
        probability_of_visiting_nurse = model_parameters.probability_of_visiting_nurse_other
        probability_of_needing_long_blood_test = model_parameters.probability_of_needing_long_blood_test
        probability_of_complex_patient = model_parameters.probability_of_complex_other_patient

        for arrival_time in patient_arrival_times:
            patients.append(OtherPatient(create_patient_schedule(arrival_time),
                                         doctor_name,
                                         probability_of_complex_patient,
                                         probability_of_visiting_nurse,
                                         probability_of_needing_long_blood_test))
    
    for patient in patients:
        patient.schedule_arrival(calendar)
        
    return patients

def layered_patient_arrival_schedule(num_patients: int, start: int = 30, end: int = 270, interval: int = 20) -> list[int]:
    """
    Schedule patients:
    1. First pass: every `interval` minutes starting from `start`
    2. Second pass: every `2*interval` minutes from `start`
    3. Third pass: every `2*interval` minutes from `start + interval`
    """
    # First pass
    layer1 = list(range(start, end + 1, interval))

    # Second pass: double-spacing from start
    layer2 = list(range(start, end + 1, 2 * interval))

    # Third pass: double-spacing from start + interval
    layer3 = list(range(start + interval, end + 1, 2 * interval))
    all_slots = layer1 + layer2 + layer3
    return all_slots[:num_patients]


def generate_patients(calendar: SimClasses.EventCalendar,parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):

    
    leukemia_doctor_1_patients = initialize_patients(
        layered_patient_arrival_schedule(
            randomize_number_of_patients(parameters.leukemia_doctor_1_number_of_regular_patients + parameters.leukemia_doctor_1_number_of_complex_patients)
        ),
        "leukemia_doctor_1", calendar, parameters
    )

    leukemia_doctor_2_patients = initialize_patients(
        layered_patient_arrival_schedule(
            randomize_number_of_patients(parameters.leukemia_doctor_2_number_of_regular_patients + parameters.leukemia_doctor_2_number_of_complex_patients)
        ),
        "leukemia_doctor_2", calendar, parameters
    )

    transplant_doctor_1_patients = initialize_patients(
        layered_patient_arrival_schedule(
            randomize_number_of_patients(parameters.transplant_doctor_1_number_of_regular_patients + parameters.transplant_doctor_1_number_of_complex_patients)
        ),
        "transplant_doctor_1", calendar, parameters
    )

    transplant_doctor_2_patients = initialize_patients(
        layered_patient_arrival_schedule(
            randomize_number_of_patients(parameters.transplant_doctor_2_number_of_regular_patients + parameters.transplant_doctor_2_number_of_complex_patients)
        ),
        "transplant_doctor_2", calendar, parameters
    )

    transplant_doctor_3_patients = initialize_patients(
        layered_patient_arrival_schedule(
            randomize_number_of_patients(parameters.transplant_doctor_3_number_of_regular_patients + parameters.transplant_doctor_3_number_of_complex_patients)
        ),
        "transplant_doctor_3", calendar, parameters
    )

    other_patients_arrival_times = layered_patient_arrival_schedule(parameters.number_of_other_patients)
    other_patients = initialize_patients(other_patients_arrival_times, "other", calendar, parameters)

    return [
        leukemia_doctor_1_patients,
        leukemia_doctor_2_patients,
        transplant_doctor_1_patients,
        transplant_doctor_2_patients,
        transplant_doctor_3_patients,
        other_patients,
    ]

def personalize_patient_schedule(current_patient: Patient, next_patient: Patient | None, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):
    complexity_level = current_patient.complexity_level
    if next_patient is None or complexity_level == "regular":
        return
    else:
        nurse_regular_service_time = np.random.exponential(model_parameters.nurse_mean_service_time_regular)
        nurse_complex_service_time = np.random.exponential(model_parameters.nurse_mean_service_time_complex)
        time_to_add = nurse_complex_service_time - nurse_regular_service_time
        next_patient.set_scheduled_arrival_time(current_patient.scheduled_arrival_time + time_to_add)

def schedule_long_nurse_service_times(list_of_patients: list[Patient], model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):
    n = len(list_of_patients)
    for index, patient in enumerate(list_of_patients):
        if index == n - 1:
            personalize_patient_schedule(patient, None, model_parameters)
        else:
            personalize_patient_schedule(patient, list_of_patients[index + 1], model_parameters)

def schedule_patient_arrival(patient: Patient, calendar: SimClasses.EventCalendar):
    patient.schedule_arrival(calendar)

def get_nurse_number_of_patients_multi_queue(patient_list: list[Patient], nurse_name: str) -> int:
    if nurse_name == "nurse_station_1":
        return len([patient for patient in patient_list if patient.nurse_name == "nurse_station_1"])
    elif nurse_name == "nurse_station_2":
        return len([patient for patient in patient_list if patient.nurse_name == "nurse_station_2"])
    elif nurse_name == "nurse_station_3":
        return len([patient for patient in patient_list if patient.nurse_name == "nurse_station_3"])
    elif nurse_name == "nurse_station_4":
        return len([patient for patient in patient_list if patient.nurse_name == "nurse_station_4"])
    elif nurse_name == "nurse_station_5":
        return len([patient for patient in patient_list if patient.nurse_name == "nurse_station_5"])
    elif nurse_name == "nurse_station_6":
        return len([patient for patient in patient_list if patient.nurse_name == "nurse_station_6"])
    else:
        raise ValueError(f"Invalid nurse name: {nurse_name}")

def get_nurse_number_of_patients_single_queue(patient_list: list[Patient], nurse_name: str) -> int:
    if nurse_name == "general_nurse_station":
        return len([patient for patient in patient_list if patient.nurse_name == "general_nurse_station"])
    elif nurse_name == "transplant_nurse_station":
        return len([patient for patient in patient_list if patient.nurse_name == "transplant_nurse_station"])
    else:
        raise ValueError(f"Invalid nurse name: {nurse_name}")



def q_flow_station_start_of_waiting(new_patient: Patient, clock: float, q_flow_station_queue: SimClasses.FIFOQueue, q_flow_station: SimClasses.Resource, q_flow_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    q_flow_station_queue.Add(new_patient)
    new_patient.enter_q_flow_queue(clock)
    if q_flow_station.CurrentNumBusy < q_flow_station.NumberOfUnits:
        q_flow_station.Seize(1)
        next_patient = q_flow_station_queue.Remove()
        q_flow_station_wait_time.Record(SimClasses.Clock - next_patient.enter_q_flow_queue_time)
        SimFunctions.SchedulePlus(calendar, "q_flow_station_service_start", 0, next_patient)

def q_flow_station_service_start(new_patient : Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    q_flow_service_duration = np.random.exponential(model_parameters.q_flow_mean_service_time)
    new_patient.q_flow_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "q_flow_station_service_end", q_flow_service_duration, new_patient)

def q_flow_station_service_end(new_patient: Patient, q_flow_station: SimClasses.Resource, q_flow_station_queue: SimClasses.FIFOQueue, q_flow_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    SimFunctions.SchedulePlus(calendar, "secretary_station_start_of_waiting", 0, new_patient)

    q_flow_station.Free(1)
    if q_flow_station.CurrentNumBusy < q_flow_station.NumberOfUnits and  q_flow_station_queue.NumQueue() > 0:
        q_flow_station.Seize(1)
        next_patient = q_flow_station_queue.Remove()
        q_flow_station_wait_time.Record(SimClasses.Clock - next_patient.enter_q_flow_queue_time)
        SimFunctions.SchedulePlus(calendar, "q_flow_station_service_start", 0, next_patient)

def secretary_station_start_of_waiting(new_patient: Patient, clock: float, secretary_station_queue: SimClasses.FIFOQueue, secretary_station: SimClasses.Resource, secretary_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    secretary_station_queue.Add(new_patient)
    new_patient.enter_secretary_queue(clock)
    if secretary_station.CurrentNumBusy < secretary_station.NumberOfUnits:
        secretary_station.Seize(1)
        next_patient = secretary_station_queue.Remove()
        secretary_station_wait_time.Record(SimClasses.Clock - next_patient.enter_secretary_queue_time)
        SimFunctions.SchedulePlus(calendar, "secretary_station_service_start", 0, next_patient)

def secretary_station_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    secretary_station_service_duration = np.random.exponential(model_parameters.secretary_mean_service_time)
    new_patient.secretary_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "secretary_station_service_end", secretary_station_service_duration, new_patient)

def secretary_station_service_end(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, secretary_station: SimClasses.Resource, secretary_station_queue: SimClasses.FIFOQueue, secretary_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    has_nurse_appointment = new_patient.visits_nurse
    if has_nurse_appointment:
        nurse_station = new_patient.nurse_name
        SimFunctions.SchedulePlus(calendar, f'{nurse_station}_start_of_waiting', 0, new_patient)
    else:
        SimFunctions.SchedulePlus(calendar, f'{new_patient.doctor_name}_start_of_waiting', 0, new_patient)
    
    secretary_station.Free(1)
    if secretary_station.CurrentNumBusy < secretary_station.NumberOfUnits and secretary_station_queue.NumQueue() > 0:
        secretary_station.Seize(1)
        next_patient = secretary_station_queue.Remove()
        secretary_station_wait_time.Record(SimClasses.Clock - next_patient.enter_secretary_queue_time)
        SimFunctions.SchedulePlus(calendar, "secretary_station_service_start", 0, next_patient)

def nurse_station_1_start_of_waiting(new_patient: Patient, clock: float, nurse_station_1_queue: SimClasses.FIFOQueue, nurse_station_1: SimClasses.Resource, nurse_station_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_1_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if nurse_station_1.CurrentNumBusy < nurse_station_1.NumberOfUnits:
        nurse_station_1.Seize(1)
        next_patient = nurse_station_1_queue.Remove()
        nurse_station_1_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_1_service_start", 0, next_patient)

def nurse_station_2_start_of_waiting(new_patient: Patient, clock: float, nurse_station_2_queue: SimClasses.FIFOQueue, nurse_station_2: SimClasses.Resource, nurse_station_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_2_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if nurse_station_2.CurrentNumBusy < nurse_station_2.NumberOfUnits:
        nurse_station_2.Seize(1)
        next_patient = nurse_station_2_queue.Remove()
        nurse_station_2_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_2_service_start", 0, next_patient)

def nurse_station_3_start_of_waiting(new_patient: Patient, clock: float, nurse_station_3_queue: SimClasses.FIFOQueue, nurse_station_3: SimClasses.Resource, nurse_station_3_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_3_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if nurse_station_3.CurrentNumBusy < nurse_station_3.NumberOfUnits:
        nurse_station_3.Seize(1)
        next_patient = nurse_station_3_queue.Remove()
        nurse_station_3_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_3_service_start", 0, next_patient)

def nurse_station_4_start_of_waiting(new_patient: Patient, clock: float, nurse_station_4_queue: SimClasses.FIFOQueue, nurse_station_4: SimClasses.Resource, nurse_station_4_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_4_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if nurse_station_4.CurrentNumBusy < nurse_station_4.NumberOfUnits:
        nurse_station_4.Seize(1)
        next_patient = nurse_station_4_queue.Remove()
        nurse_station_4_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_4_service_start", 0, next_patient)

def nurse_station_5_start_of_waiting(new_patient: Patient, clock: float, nurse_station_5_queue: SimClasses.FIFOQueue, nurse_station_5: SimClasses.Resource, nurse_station_5_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_5_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if nurse_station_5.CurrentNumBusy < nurse_station_5.NumberOfUnits:
        nurse_station_5.Seize(1)
        next_patient = nurse_station_5_queue.Remove()
        nurse_station_5_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_5_service_start", 0, next_patient)

def nurse_station_6_start_of_waiting(new_patient: Patient, clock: float, nurse_station_6_queue: SimClasses.FIFOQueue, nurse_station_6: SimClasses.Resource, nurse_station_6_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_6_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if nurse_station_6.CurrentNumBusy < nurse_station_6.NumberOfUnits:
        nurse_station_6.Seize(1)
        next_patient = nurse_station_6_queue.Remove()
        nurse_station_6_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_6_service_start", 0, next_patient)

def nurse_station_1_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)

    SimFunctions.SchedulePlus(calendar, "nurse_station_1_service_end", service_duration, new_patient)

def nurse_station_2_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "nurse_station_2_service_end", service_duration, new_patient)

def nurse_station_3_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "nurse_station_3_service_end", service_duration, new_patient)

def nurse_station_4_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "nurse_station_4_service_end", service_duration, new_patient)

def nurse_station_5_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "nurse_station_5_service_end", service_duration, new_patient)

def nurse_station_6_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    mean_service_time = model_parameters.nurse_mean_service_time_complex
    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "nurse_station_6_service_end", service_duration, new_patient)

def nurse_station_1_service_end(new_patient: Patient, nurse_station_1: SimClasses.Resource, nurse_station_1_queue: SimClasses.FIFOQueue, nurse_station_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_1.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if nurse_station_1.CurrentNumBusy < nurse_station_1.NumberOfUnits and nurse_station_1_queue.NumQueue() > 0:
        nurse_station_1.Seize(1)
        next_patient = nurse_station_1_queue.Remove()
        nurse_station_1_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_1_service_start", 0, next_patient)

def nurse_station_2_service_end(new_patient: Patient, nurse_station_2: SimClasses.Resource, nurse_station_2_queue: SimClasses.FIFOQueue, nurse_station_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_2.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if nurse_station_2.CurrentNumBusy < nurse_station_2.NumberOfUnits and nurse_station_2_queue.NumQueue() > 0:
        nurse_station_2.Seize(1)
        next_patient = nurse_station_2_queue.Remove()
        nurse_station_2_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_2_service_start", 0, next_patient)

def nurse_station_3_service_end(new_patient: Patient, nurse_station_3: SimClasses.Resource, nurse_station_3_queue: SimClasses.FIFOQueue, nurse_station_3_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_3.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if nurse_station_3.CurrentNumBusy < nurse_station_3.NumberOfUnits and nurse_station_3_queue.NumQueue() > 0:
        nurse_station_3.Seize(1)
        next_patient = nurse_station_3_queue.Remove()
        nurse_station_3_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_3_service_start", 0, next_patient)

def nurse_station_4_service_end(new_patient: Patient, nurse_station_4: SimClasses.Resource, nurse_station_4_queue: SimClasses.FIFOQueue, nurse_station_4_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_4.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if nurse_station_4.CurrentNumBusy < nurse_station_4.NumberOfUnits and nurse_station_4_queue.NumQueue() > 0:
        nurse_station_4.Seize(1)
        next_patient = nurse_station_4_queue.Remove()
        nurse_station_4_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_4_service_start", 0, next_patient)

def nurse_station_5_service_end(new_patient: Patient, nurse_station_5: SimClasses.Resource, nurse_station_5_queue: SimClasses.FIFOQueue, nurse_station_5_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_5.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if nurse_station_5.CurrentNumBusy < nurse_station_5.NumberOfUnits and nurse_station_5_queue.NumQueue() > 0:
        nurse_station_5.Seize(1)
        next_patient = nurse_station_5_queue.Remove()
        nurse_station_5_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_5_service_start", 0, next_patient)

def nurse_station_6_service_end(new_patient: Patient, nurse_station_6: SimClasses.Resource, nurse_station_6_queue: SimClasses.FIFOQueue, nurse_station_6_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    nurse_station_6.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if nurse_station_6.CurrentNumBusy < nurse_station_6.NumberOfUnits and nurse_station_6_queue.NumQueue() > 0:
        nurse_station_6.Seize(1)
        next_patient = nurse_station_6_queue.Remove()
        nurse_station_6_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "nurse_station_6_service_start", 0, next_patient)

def leukemia_doctor_1_start_of_waiting(new_patient: Patient, clock: float, leukemia_doctor_1_queue: SimClasses.FIFOQueue, leukemia_doctor_1: SimClasses.Resource, leukemia_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar, doctors_start_service: bool):
    leukemia_doctor_1_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if leukemia_doctor_1.CurrentNumBusy < leukemia_doctor_1.NumberOfUnits and doctors_start_service:
        next_patient = leukemia_doctor_1_queue.Remove()
        if next_patient is not None:
            leukemia_doctor_1.Seize(1)
            leukemia_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "leukemia_doctor_1_service_start", 0, next_patient)    

def leukemia_doctor_2_start_of_waiting(new_patient: Patient, clock: float, leukemia_doctor_2_queue: SimClasses.FIFOQueue, leukemia_doctor_2: SimClasses.Resource, leukemia_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar, doctors_start_service: bool):
    leukemia_doctor_2_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if leukemia_doctor_2.CurrentNumBusy < leukemia_doctor_2.NumberOfUnits and doctors_start_service:
        next_patient = leukemia_doctor_2_queue.Remove()
        if next_patient is not None:
            leukemia_doctor_2.Seize(1)
            leukemia_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "leukemia_doctor_2_service_start", 0, next_patient)

def transplant_doctor_1_start_of_waiting(new_patient: Patient, clock: float, transplant_doctor_1_queue: SimClasses.FIFOQueue, transplant_doctor_1: SimClasses.Resource, transplant_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar, doctors_start_service: bool):
    transplant_doctor_1_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if transplant_doctor_1.CurrentNumBusy < transplant_doctor_1.NumberOfUnits and doctors_start_service:
        next_patient = transplant_doctor_1_queue.Remove()
        if next_patient is not None:
            transplant_doctor_1.Seize(1)
            transplant_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "transplant_doctor_1_service_start", 0, next_patient)

def transplant_doctor_2_start_of_waiting(new_patient: Patient, clock: float, transplant_doctor_2_queue: SimClasses.FIFOQueue, transplant_doctor_2: SimClasses.Resource, transplant_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar, doctors_start_service: bool):
    transplant_doctor_2_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if transplant_doctor_2.CurrentNumBusy < transplant_doctor_2.NumberOfUnits and doctors_start_service:
        next_patient = transplant_doctor_2_queue.Remove()
        if next_patient is not None:
            transplant_doctor_2.Seize(1)
            transplant_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "transplant_doctor_2_service_start", 0, next_patient)

def transplant_doctor_3_start_of_waiting(new_patient: Patient, clock: float, transplant_doctor_3_queue: SimClasses.FIFOQueue, transplant_doctor_3: SimClasses.Resource, transplant_doctor_3_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar, doctors_start_service: bool):
    transplant_doctor_3_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if transplant_doctor_3.CurrentNumBusy < transplant_doctor_3.NumberOfUnits and doctors_start_service:
        next_patient = transplant_doctor_3_queue.Remove()
        if next_patient is not None:
            transplant_doctor_3.Seize(1)
            transplant_doctor_3_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "transplant_doctor_3_service_start", 0, next_patient)

def other_doctor_start_of_waiting(new_patient: Patient, clock: float, other_doctor_queue: SimClasses.FIFOQueue, other_doctor: SimClasses.Resource, other_doctor_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    new_patient.enter_doctor_queue(clock)
    #other patients doctor treatment is not included in the model
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

def set_patient_blood_test_results_ready_time(new_patient: Patient, calendar: SimClasses.EventCalendar, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):
    needs_long_blood_test = new_patient.needs_long_blood_test
    if needs_long_blood_test:
        time_for_blood_test_results = np.random.exponential(model_parameters.mean_time_for_long_blood_test)
    else:
        time_for_blood_test_results = np.random.exponential(model_parameters.mean_time_for_regular_blood_test)
    SimFunctions.SchedulePlus(calendar, "receive_blood_test_results", time_for_blood_test_results, new_patient)
    # Schedule a check of the doctor's queue when blood test results are ready
    SimFunctions.SchedulePlus(calendar, f"{new_patient.doctor_name}_start_of_waiting", time_for_blood_test_results, new_patient)

def leukemia_doctor_1_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level
    new_patient.doctor_service_start(SimClasses.Clock)
    if patient_complexity == "regular":
        mean_service_time = model_parameters.leukemia_doctor_1_mean_service_time_regular
    else:
        mean_service_time = model_parameters.leukemia_doctor_1_mean_service_time_complex
    service_duration = np.random.exponential(mean_service_time)
    SimFunctions.SchedulePlus(calendar, "leukemia_doctor_1_service_end", service_duration, new_patient)

def leukemia_doctor_2_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level
    new_patient.doctor_service_start(SimClasses.Clock)
    if patient_complexity == "regular":
        mean_service_time = model_parameters.leukemia_doctor_2_mean_service_time_regular
    else:
        mean_service_time = model_parameters.leukemia_doctor_2_mean_service_time_complex
    service_duration = np.random.exponential(mean_service_time)
    SimFunctions.SchedulePlus(calendar, "leukemia_doctor_2_service_end", service_duration, new_patient)

def transplant_doctor_1_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level
    new_patient.doctor_service_start(SimClasses.Clock)
    if patient_complexity == "regular":
        mean_service_time = model_parameters.transplant_doctor_1_mean_service_time_regular
    else:
        mean_service_time = model_parameters.transplant_doctor_1_mean_service_time_complex
    service_duration = np.random.exponential(mean_service_time)
    SimFunctions.SchedulePlus(calendar, "transplant_doctor_1_service_end", service_duration, new_patient)

def transplant_doctor_2_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level
    new_patient.doctor_service_start(SimClasses.Clock)
    if patient_complexity == "regular":
        mean_service_time = model_parameters.transplant_doctor_2_mean_service_time_regular
    else:
        mean_service_time = model_parameters.transplant_doctor_2_mean_service_time_complex
    service_duration = np.random.exponential(mean_service_time)
    SimFunctions.SchedulePlus(calendar, "transplant_doctor_2_service_end", service_duration, new_patient)

def transplant_doctor_3_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level
    new_patient.doctor_service_start(SimClasses.Clock)
    if patient_complexity == "regular":
        mean_service_time = model_parameters.transplant_doctor_3_mean_service_time_regular
    else:
        mean_service_time = model_parameters.transplant_doctor_3_mean_service_time_complex
    service_duration = np.random.exponential(mean_service_time)
    SimFunctions.SchedulePlus(calendar, "transplant_doctor_3_service_end", service_duration, new_patient)

def leukemia_doctor_1_service_end(new_patient: Patient, leukemia_doctor_1: SimClasses.Resource, leukemia_doctor_1_queue: SimClasses.FIFOQueue, leukemia_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    leukemia_doctor_1.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if leukemia_doctor_1.CurrentNumBusy < leukemia_doctor_1.NumberOfUnits and leukemia_doctor_1_queue.NumQueue() > 0:
        next_patient = leukemia_doctor_1_queue.Remove()
        if next_patient is not None:
            leukemia_doctor_1.Seize(1)
            leukemia_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "leukemia_doctor_1_service_start", 0, next_patient)

def leukemia_doctor_2_service_end(new_patient: Patient, leukemia_doctor_2: SimClasses.Resource, leukemia_doctor_2_queue: SimClasses.FIFOQueue, leukemia_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    leukemia_doctor_2.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if leukemia_doctor_2.CurrentNumBusy < leukemia_doctor_2.NumberOfUnits and leukemia_doctor_2_queue.NumQueue() > 0:
        next_patient = leukemia_doctor_2_queue.Remove()
        if next_patient is not None:
            leukemia_doctor_2.Seize(1)
            leukemia_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "leukemia_doctor_2_service_start", 0, next_patient)

def transplant_doctor_1_service_end(new_patient: Patient, transplant_doctor_1: SimClasses.Resource, transplant_doctor_1_queue: SimClasses.FIFOQueue, transplant_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_1.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if transplant_doctor_1.CurrentNumBusy < transplant_doctor_1.NumberOfUnits and transplant_doctor_1_queue.NumQueue() > 0:
        next_patient = transplant_doctor_1_queue.Remove()
        if next_patient is not None:
            transplant_doctor_1.Seize(1)
            transplant_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "transplant_doctor_1_service_start", 0, next_patient)

def transplant_doctor_2_service_end(new_patient: Patient, transplant_doctor_2: SimClasses.Resource, transplant_doctor_2_queue: SimClasses.FIFOQueue, transplant_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_2.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if transplant_doctor_2.CurrentNumBusy < transplant_doctor_2.NumberOfUnits and transplant_doctor_2_queue.NumQueue() > 0:
        next_patient = transplant_doctor_2_queue.Remove()
        if next_patient is not None:
            transplant_doctor_2.Seize(1)
            transplant_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "transplant_doctor_2_service_start", 0, next_patient)

def transplant_doctor_3_service_end(new_patient: Patient, transplant_doctor_3: SimClasses.Resource, transplant_doctor_3_queue: SimClasses.FIFOQueue, transplant_doctor_3_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_3.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if transplant_doctor_3.CurrentNumBusy < transplant_doctor_3.NumberOfUnits and transplant_doctor_3_queue.NumQueue() > 0:
        next_patient = transplant_doctor_3_queue.Remove()
        if next_patient is not None:
            transplant_doctor_3.Seize(1)
            transplant_doctor_3_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, "transplant_doctor_3_service_start", 0, next_patient)

def process_complete(new_patient: Patient, clock: float, nurse_station_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, nurse_station_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, nurse_station_3_scheduled_vs_actual_time_diff: SimClasses.DTStat, nurse_station_4_scheduled_vs_actual_time_diff: SimClasses.DTStat, nurse_station_5_scheduled_vs_actual_time_diff: SimClasses.DTStat, nurse_station_6_scheduled_vs_actual_time_diff: SimClasses.DTStat,
                      leukemia_doctor_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, leukemia_doctor_1_complex_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_1_regular_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, leukemia_doctor_2_complex_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_2_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_1_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_1_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_2_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_2_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_3_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_3_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_3_regular_patients_total_processing_time: SimClasses.DTStat, other_patients_total_processing_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    if new_patient.doctor_name == "leukemia_doctor_1":
        leukemia_doctor_1_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            leukemia_doctor_1_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            leukemia_doctor_1_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "leukemia_doctor_2":
        leukemia_doctor_2_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            leukemia_doctor_2_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            leukemia_doctor_2_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "transplant_doctor_1":
        transplant_doctor_1_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            transplant_doctor_1_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            transplant_doctor_1_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "transplant_doctor_2":
        transplant_doctor_2_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            transplant_doctor_2_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            transplant_doctor_2_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "transplant_doctor_3":
        transplant_doctor_3_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            transplant_doctor_3_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            transplant_doctor_3_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "other":
        other_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    else:
        raise ValueError(f"Invalid doctor name: {new_patient.doctor_name}")
    
    if new_patient.nurse_name == "nurse_station_1":
        nurse_station_1_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    elif new_patient.nurse_name == "nurse_station_2":
        nurse_station_2_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    elif new_patient.nurse_name == "nurse_station_3":
        nurse_station_3_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    elif new_patient.nurse_name == "nurse_station_4":
        nurse_station_4_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    elif new_patient.nurse_name == "nurse_station_5":
        nurse_station_5_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    elif new_patient.nurse_name == "nurse_station_6":
        nurse_station_6_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    
    new_patient.end_visit(clock)

def process_complete_single_queue(new_patient: Patient, clock: float, general_nurse_station_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_nurse_station_scheduled_vs_actual_time_diff: SimClasses.DTStat,
                      leukemia_doctor_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, leukemia_doctor_1_complex_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_1_regular_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, leukemia_doctor_2_complex_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_2_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_1_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_1_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_2_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_2_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_3_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_3_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_3_regular_patients_total_processing_time: SimClasses.DTStat, other_patients_total_processing_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    if new_patient.doctor_name == "leukemia_doctor_1":
        leukemia_doctor_1_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            leukemia_doctor_1_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            leukemia_doctor_1_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "leukemia_doctor_2":
        leukemia_doctor_2_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            leukemia_doctor_2_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            leukemia_doctor_2_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "transplant_doctor_1":
        transplant_doctor_1_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            transplant_doctor_1_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            transplant_doctor_1_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "transplant_doctor_2":
        transplant_doctor_2_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            transplant_doctor_2_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            transplant_doctor_2_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "transplant_doctor_3":
        transplant_doctor_3_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time)
        if new_patient.complexity_level == "complex":
            transplant_doctor_3_complex_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
        else:
            transplant_doctor_3_regular_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    elif new_patient.doctor_name == "other":
        other_patients_total_processing_time.Record(SimClasses.Clock - new_patient.arrival_time)
    else:
        raise ValueError(f"Invalid doctor name: {new_patient.doctor_name}")
    
    if new_patient.nurse_name == "general_nurse_station":
        general_nurse_station_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    elif new_patient.nurse_name == "transplant_nurse_station":
        transplant_nurse_station_scheduled_vs_actual_time_diff.Record(new_patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time)
    
    new_patient.end_visit(clock)

def assign_nurse_station_single_queue(patient_type: str, patient_complexity: str, parameters: ModelParametersSingleQueue) -> str:
    u = random.uniform(0, 1)
    if patient_type == "transplant" and patient_complexity == "regular":
        p_1 = parameters.general_nurse_station_assignment_probability_transplant_regular
        p_2 = parameters.transplant_nurse_station_assignment_probability_transplant_regular
        if u < p_1:
            return "general_nurse_station"
        elif u <= p_1 + p_2:
            return "transplant_nurse_station"
        else:
            raise ValueError("Issue with Transplant nurse assignment probabilities")
        
    elif patient_type == "transplant":
        return "transplant_nurse_station"

    else:
        return "general_nurse_station"
        
def general_nurse_station_start_of_waiting(new_patient: Patient, clock: float, model_parameters: ModelParametersSingleQueue, general_nurse_station_queue: SimClasses.FIFOQueue, general_nurse_station: SimClasses.Resource, general_nurse_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    general_nurse_station_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if general_nurse_station.CurrentNumBusy < general_nurse_station.NumberOfUnits:
        general_nurse_station.Seize(1)
        next_patient = general_nurse_station_queue.Remove()
        general_nurse_station_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "general_nurse_station_service_start", model_parameters.general_nurse_station_preparation_time_buffer, next_patient)


def general_nurse_station_service_start(new_patient: Patient, model_parameters: ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "general_nurse_station_service_end", service_duration, new_patient)

def general_nurse_station_service_end(new_patient: Patient, general_nurse_station: SimClasses.Resource, general_nurse_station_queue: SimClasses.FIFOQueue, general_nurse_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    general_nurse_station.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if general_nurse_station.CurrentNumBusy < general_nurse_station.NumberOfUnits and general_nurse_station_queue.NumQueue() > 0:
        general_nurse_station.Seize(1)
        next_patient = general_nurse_station_queue.Remove()
        general_nurse_station_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "general_nurse_station_service_start", 0, next_patient)

def transplant_nurse_station_start_of_waiting(new_patient: Patient, clock: float, transplant_nurse_station_queue: SimClasses.FIFOQueue, transplant_nurse_station: SimClasses.Resource, transplant_nurse_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_nurse_station_queue.Add(new_patient)
    new_patient.enter_nurse_queue(clock)
    if transplant_nurse_station.CurrentNumBusy < transplant_nurse_station.NumberOfUnits:
        transplant_nurse_station.Seize(1)
        next_patient = transplant_nurse_station_queue.Remove()
        transplant_nurse_station_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_nurse_station_service_start", 0, next_patient)

def transplant_nurse_station_service_start(new_patient: Patient, model_parameters: ModelParametersSingleQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)
    new_patient.nurse_service_start(SimClasses.Clock)
    SimFunctions.SchedulePlus(calendar, "transplant_nurse_station_service_end", service_duration, new_patient)

def transplant_nurse_station_service_end(new_patient: Patient, transplant_nurse_station: SimClasses.Resource, transplant_nurse_station_queue: SimClasses.FIFOQueue, transplant_nurse_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_nurse_station.Free(1)
    doctor_name = new_patient.doctor_name
    SimFunctions.SchedulePlus(calendar, f"{doctor_name}_start_of_waiting", 0, new_patient)

    if transplant_nurse_station.CurrentNumBusy < transplant_nurse_station.NumberOfUnits and transplant_nurse_station_queue.NumQueue() > 0:
        transplant_nurse_station.Seize(1)
        next_patient = transplant_nurse_station_queue.Remove()
        transplant_nurse_station_wait_time.Record(SimClasses.Clock - next_patient.enter_nurse_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_nurse_station_service_start", 0, next_patient)

def schedule_doctor_service_start_time(calendar: SimClasses.EventCalendar, schedule_start_time: int):
    SimFunctions.Schedule(calendar, f"set_doctor_service_start_flag_to_true", schedule_start_time)

def generate_patient_attributes_csv(patients: list[list[Patient]], output_path: str = "results_directory/patient_attributes.csv"):
    """
    Generate a CSV file containing all attributes of patients from the simulation.
    
    Args:
        patients: List of lists containing Patient objects
        output_path: Path where the CSV file should be saved
    """
    # Flatten the list of lists into a single list of patients
    all_patients = [patient for patient_list in patients for patient in patient_list]
    
    # Create a list of dictionaries containing patient attributes
    patient_data = []
    for patient in all_patients:
        doctor_scheduled_vs_actual_time_diff = None
        nurse_scheduled_vs_actual_time_diff = None
        if patient.get_type() != "other":
            doctor_scheduled_vs_actual_time_diff = patient.scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time
        if patient.visits_nurse:
            nurse_scheduled_vs_actual_time_diff = patient.scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time
        patient_dict = {
            'Patient Type': patient.get_type(),
            'Doctor Name': patient.doctor_name,
            'Complexity Level': patient.complexity_level,
            'Visits Nurse': patient.visits_nurse,
            'Nurse Name': patient.nurse_name,
            'Needs Long Blood Test': patient.needs_long_blood_test,
            'Arrival Time': patient.arrival_time,
            'Q-Flow Queue Entry Time': patient.enter_q_flow_queue_time,
            'Q-Flow Service Start Time': patient.q_flow_service_start_time,
            'Secretary Queue Entry Time': patient.enter_secretary_queue_time,
            'Secretary Service Start Time': patient.secretary_service_start_time,
            'Nurse Queue Entry Time': patient.enter_nurse_queue_time,
            'Nurse Service Start Time': patient.nurse_service_start_time,
            'Doctor Queue Entry Time': patient.enter_doctor_queue_time,
            'End of Visit Time': patient.end_of_visit_time,
            'Scheduled vs Actual Nurse Time Diff': nurse_scheduled_vs_actual_time_diff,
            'Scheduled vs Actual Doctor Time Diff': doctor_scheduled_vs_actual_time_diff
        }
        patient_data.append(patient_dict)
    
    # Create DataFrame
    df = pd.DataFrame(patient_data)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Patient attributes saved to {output_path}")

def check_doctor_queue_and_start_service(doctor: SimClasses.Resource, doctor_queue: SimClasses.FIFOQueue, doctor_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar, doctor_name: str):
    """
    Check if a doctor is idle and has patients waiting, and if so, start serving the next patient.
    
    Args:
        doctor: The doctor resource
        doctor_queue: The doctor's queue
        doctor_wait_time: The wait time statistic for this doctor
        calendar: The simulation calendar
        doctor_name: The name of the doctor (e.g. "leukemia_doctor_1")
    """
    if doctor.CurrentNumBusy < doctor.NumberOfUnits and doctor_queue.NumQueue() > 0:
        next_patient = doctor_queue.Remove()
        if next_patient is not None:
            doctor.Seize(1)
            doctor_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
            SimFunctions.SchedulePlus(calendar, f"{doctor_name}_service_start", 0, next_patient)