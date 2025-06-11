from model_parameters import ModelParametersMultiQueue, ModelParametersSingleQueue
import numpy as np
import numpy.random as random
from patients.patient import Patient
from patients.leukemia_patient import LeukemiaPatient
from patients.transplant_patient import TransplantPatient
from patients.other_patient import OtherPatient
from python_sim import SimClasses
from python_sim import SimFunctions

def assign_nurse_station_multi_queue(patient_type: str, parameters: ModelParametersMultiQueue) -> str:
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
        elif u <= p_1 + p_2 + p_3 + p_4 + p_5:
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
        elif u <= p_1 + p_2 + p_3 + p_4 + p_5:
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
                        model_parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):
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

def generate_patients(calendar: SimClasses.EventCalendar,parameters: ModelParametersMultiQueue | ModelParametersSingleQueue):
    
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
    SimFunctions.SchedulePlus(calendar, "secretary_station_service_end", secretary_station_service_duration, new_patient)

def secretary_station_service_end_multi_queue(new_patient: Patient, model_parameters: ModelParametersMultiQueue, secretary_station: SimClasses.Resource, secretary_station_queue: SimClasses.FIFOQueue, secretary_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    patient_type = new_patient.get_type()
    has_nurse_appointment = new_patient.visits_nurse
    if has_nurse_appointment:
        nurse_station = assign_nurse_station_multi_queue(patient_type, model_parameters)
        SimFunctions.SchedulePlus(calendar, f'{nurse_station}_start_of_waiting', 0, new_patient)
    else:
        SimFunctions.SchedulePlus(calendar, f'{new_patient.doctor_name}_start_of_waiting', 0, new_patient)
    
    secretary_station.Free(1)
    if secretary_station.CurrentNumBusy < secretary_station.NumberOfUnits and secretary_station_queue.NumQueue() > 0:
        secretary_station.Seize(1)
        next_patient = secretary_station_queue.Remove()
        secretary_station_wait_time.Record(SimClasses.Clock - next_patient.enter_secretary_queue_time)
        SimFunctions.SchedulePlus(calendar, "secretary_station_service_start", 0, next_patient)

def secretary_station_service_end_single_queue(new_patient: Patient, model_parameters: ModelParametersSingleQueue, secretary_station: SimClasses.Resource, secretary_station_queue: SimClasses.FIFOQueue, secretary_station_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    patient_type = new_patient.get_type()
    has_nurse_appointment = new_patient.visits_nurse
    if has_nurse_appointment:
        nurse_station = assign_nurse_station_single_queue(patient_type, model_parameters)
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

    SimFunctions.SchedulePlus(calendar, "nurse_station_1_service_end", service_duration, new_patient)

def nurse_station_2_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)

    SimFunctions.SchedulePlus(calendar, "nurse_station_2_service_end", service_duration, new_patient)

def nurse_station_3_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)

    SimFunctions.SchedulePlus(calendar, "nurse_station_3_service_end", service_duration, new_patient)

def nurse_station_4_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)

    SimFunctions.SchedulePlus(calendar, "nurse_station_4_service_end", service_duration, new_patient)

def nurse_station_5_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)

    SimFunctions.SchedulePlus(calendar, "nurse_station_5_service_end", service_duration, new_patient)

def nurse_station_6_service_start(new_patient: Patient, model_parameters: ModelParametersMultiQueue, calendar: SimClasses.EventCalendar):
    patient_complexity = new_patient.complexity_level

    if patient_complexity == "regular":
        mean_service_time = model_parameters.nurse_mean_service_time_regular
    else:
        mean_service_time = model_parameters.nurse_mean_service_time_complex

    service_duration = np.random.exponential(mean_service_time)

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

def leukemia_doctor_1_start_of_waiting(new_patient: Patient, clock: float, leukemia_doctor_1_queue: SimClasses.FIFOQueue, leukemia_doctor_1: SimClasses.Resource, leukemia_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    leukemia_doctor_1_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if leukemia_doctor_1.CurrentNumBusy < leukemia_doctor_1.NumberOfUnits:
        leukemia_doctor_1.Seize(1)
        next_patient = leukemia_doctor_1_queue.Remove()
        leukemia_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "leukemia_doctor_1_service_start", 0, next_patient)

def leukemia_doctor_2_start_of_waiting(new_patient: Patient, clock: float, leukemia_doctor_2_queue: SimClasses.FIFOQueue, leukemia_doctor_2: SimClasses.Resource, leukemia_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    leukemia_doctor_2_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if leukemia_doctor_2.CurrentNumBusy < leukemia_doctor_2.NumberOfUnits:
        leukemia_doctor_2.Seize(1)
        next_patient = leukemia_doctor_2_queue.Remove()
        leukemia_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "leukemia_doctor_2_service_start", 0, next_patient)

def transplant_doctor_1_start_of_waiting(new_patient: Patient, clock: float, transplant_doctor_1_queue: SimClasses.FIFOQueue, transplant_doctor_1: SimClasses.Resource, transplant_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_1_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if transplant_doctor_1.CurrentNumBusy < transplant_doctor_1.NumberOfUnits:
        transplant_doctor_1.Seize(1)
        next_patient = transplant_doctor_1_queue.Remove()
        transplant_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_doctor_1_service_start", 0, next_patient)

def transplant_doctor_2_start_of_waiting(new_patient: Patient, clock: float, transplant_doctor_2_queue: SimClasses.FIFOQueue, transplant_doctor_2: SimClasses.Resource, transplant_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_2_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if transplant_doctor_2.CurrentNumBusy < transplant_doctor_2.NumberOfUnits:
        transplant_doctor_2.Seize(1)
        next_patient = transplant_doctor_2_queue.Remove()
        transplant_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_doctor_2_service_start", 0, next_patient)

def transplant_doctor_3_start_of_waiting(new_patient: Patient, clock: float, transplant_doctor_3_queue: SimClasses.FIFOQueue, transplant_doctor_3: SimClasses.Resource, transplant_doctor_3_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_3_queue.Add(new_patient)
    new_patient.enter_doctor_queue(clock)
    if transplant_doctor_3.CurrentNumBusy < transplant_doctor_3.NumberOfUnits:
        transplant_doctor_3.Seize(1)
        next_patient = transplant_doctor_3_queue.Remove()
        transplant_doctor_3_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_doctor_3_service_start", 0, next_patient)

def other_doctor_start_of_waiting(new_patient: Patient, clock: float, other_doctor_queue: SimClasses.FIFOQueue, other_doctor: SimClasses.Resource, other_doctor_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    new_patient.enter_doctor_queue(clock)
    #other patients doctor treatment is not included in the model
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

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
        leukemia_doctor_1.Seize(1)
        next_patient = leukemia_doctor_1_queue.Remove()
        leukemia_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "leukemia_doctor_1_service_start", 0, next_patient)

def leukemia_doctor_2_service_end(new_patient: Patient, leukemia_doctor_2: SimClasses.Resource, leukemia_doctor_2_queue: SimClasses.FIFOQueue, leukemia_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    leukemia_doctor_2.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if leukemia_doctor_2.CurrentNumBusy < leukemia_doctor_2.NumberOfUnits and leukemia_doctor_2_queue.NumQueue() > 0:
        leukemia_doctor_2.Seize(1)
        next_patient = leukemia_doctor_2_queue.Remove()
        leukemia_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "leukemia_doctor_2_service_start", 0, next_patient)

def transplant_doctor_1_service_end(new_patient: Patient, transplant_doctor_1: SimClasses.Resource, transplant_doctor_1_queue: SimClasses.FIFOQueue, transplant_doctor_1_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_1.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if transplant_doctor_1.CurrentNumBusy < transplant_doctor_1.NumberOfUnits and transplant_doctor_1_queue.NumQueue() > 0:
        transplant_doctor_1.Seize(1)
        next_patient = transplant_doctor_1_queue.Remove()
        transplant_doctor_1_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_doctor_1_service_start", 0, next_patient)

def transplant_doctor_2_service_end(new_patient: Patient, transplant_doctor_2: SimClasses.Resource, transplant_doctor_2_queue: SimClasses.FIFOQueue, transplant_doctor_2_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_2.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if transplant_doctor_2.CurrentNumBusy < transplant_doctor_2.NumberOfUnits and transplant_doctor_2_queue.NumQueue() > 0:
        transplant_doctor_2.Seize(1)
        next_patient = transplant_doctor_2_queue.Remove()
        transplant_doctor_2_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_doctor_2_service_start", 0, next_patient)

def transplant_doctor_3_service_end(new_patient: Patient, transplant_doctor_3: SimClasses.Resource, transplant_doctor_3_queue: SimClasses.FIFOQueue, transplant_doctor_3_wait_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
    transplant_doctor_3.Free(1)
    SimFunctions.SchedulePlus(calendar, "process_complete", 0, new_patient)

    if transplant_doctor_3.CurrentNumBusy < transplant_doctor_3.NumberOfUnits and transplant_doctor_3_queue.NumQueue() > 0:
        transplant_doctor_3.Seize(1)
        next_patient = transplant_doctor_3_queue.Remove()
        transplant_doctor_3_wait_time.Record(SimClasses.Clock - next_patient.enter_doctor_queue_time)
        SimFunctions.SchedulePlus(calendar, "transplant_doctor_3_service_start", 0, next_patient)

def process_complete(new_patient: Patient, clock: float, leukemia_doctor_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, leukemia_doctor_1_complex_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_1_regular_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, leukemia_doctor_2_complex_patients_total_processing_time: SimClasses.DTStat, leukemia_doctor_2_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_1_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_1_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_1_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_2_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_2_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_2_regular_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_3_scheduled_vs_actual_time_diff: SimClasses.DTStat, transplant_doctor_3_complex_patients_total_processing_time: SimClasses.DTStat, transplant_doctor_3_regular_patients_total_processing_time: SimClasses.DTStat, other_patients_total_processing_time: SimClasses.DTStat, calendar: SimClasses.EventCalendar):
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
    
    new_patient.end_visit(clock)

def assign_nurse_station_single_queue(patient_type: str, parameters: ModelParametersSingleQueue) -> str:
    u = random.uniform(0, 1)
    if patient_type == "transplant":
        p_1 = parameters.general_nurse_station_assignment_probability_transplant
        p_2 = parameters.transplant_nurse_station_assignment_probability_transplant
        if u < p_1:
            return "general_nurse_station"
        elif u <= p_1 + p_2:
            return "transplant_nurse_station"
        else:
            raise ValueError("Issue with Transplant nurse assignment probabilities")
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