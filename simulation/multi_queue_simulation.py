import os

import pandas as pd
import numpy as np
import scipy.stats as scs
from tqdm import tqdm

from python_sim import SimFunctions, SimClasses
from model_parameters import ModelParametersMultiQueue
from simulation_configuration import SimulationConfiguration
import utils as utils
import json

def run_multi_queue_simulation(parameter_dict: dict=None):
    if parameter_dict is None:
        model_parameters = ModelParametersMultiQueue()
    else:
        model_parameters = ModelParametersMultiQueue.from_dict(parameter_dict)

    # Initializing event calendar
    Calendar = SimClasses.EventCalendar()

    simulation_configuration = SimulationConfiguration()

    q_flow_station = SimClasses.Resource()
    q_flow_station.SetUnits(1)
    q_flow_station_queue = SimClasses.FIFOQueue()

    secretary_station = SimClasses.Resource()
    secretary_station.SetUnits(2)

    secretary_station_queue = SimClasses.FIFOQueue()

    nurse_station_1 = SimClasses.Resource()
    nurse_station_1.SetUnits(1)
    nurse_station_2 = SimClasses.Resource()
    nurse_station_2.SetUnits(1)
    nurse_station_3 = SimClasses.Resource()
    nurse_station_3.SetUnits(1)
    nurse_station_4 = SimClasses.Resource()
    nurse_station_4.SetUnits(1)
    nurse_station_5 = SimClasses.Resource()
    nurse_station_5.SetUnits(1)
    nurse_station_6 = SimClasses.Resource()
    nurse_station_6.SetUnits(1)

    nurse_station_1_queue = SimClasses.FIFOQueue()
    nurse_station_2_queue = SimClasses.FIFOQueue()
    nurse_station_3_queue = SimClasses.FIFOQueue()
    nurse_station_4_queue = SimClasses.FIFOQueue()
    nurse_station_5_queue = SimClasses.FIFOQueue()
    nurse_station_6_queue = SimClasses.FIFOQueue()

    leukemia_doctor_1 = SimClasses.Resource()
    leukemia_doctor_1.SetUnits(1)
    leukemia_doctor_2 = SimClasses.Resource()
    leukemia_doctor_2.SetUnits(1)
    transplant_doctor_1 = SimClasses.Resource()
    transplant_doctor_1.SetUnits(1)
    transplant_doctor_2 = SimClasses.Resource()
    transplant_doctor_2.SetUnits(1)
    transplant_doctor_3 = SimClasses.Resource()
    transplant_doctor_3.SetUnits(1)

    leukemia_doctor_1_queue = SimClasses.ConstrainedFIFOQueue()
    leukemia_doctor_2_queue = SimClasses.ConstrainedFIFOQueue()
    transplant_doctor_1_queue = SimClasses.ConstrainedFIFOQueue()
    transplant_doctor_2_queue = SimClasses.ConstrainedFIFOQueue()
    transplant_doctor_3_queue = SimClasses.ConstrainedFIFOQueue()

    q_flow_station_wait_time = SimClasses.DTStat()

    secretary_station_wait_time = SimClasses.DTStat()

    nurse_station_1_wait_time = SimClasses.DTStat()
    nurse_station_2_wait_time = SimClasses.DTStat()
    nurse_station_3_wait_time = SimClasses.DTStat()
    nurse_station_4_wait_time = SimClasses.DTStat()
    nurse_station_5_wait_time = SimClasses.DTStat()
    nurse_station_6_wait_time = SimClasses.DTStat()

    leukemia_doctor_1_wait_time = SimClasses.DTStat()
    leukemia_doctor_2_wait_time = SimClasses.DTStat()

    transplant_doctor_1_wait_time = SimClasses.DTStat()
    transplant_doctor_2_wait_time = SimClasses.DTStat()
    transplant_doctor_3_wait_time = SimClasses.DTStat()

    leukemia_doctor_1_complex_patients_total_processing_time = SimClasses.DTStat()
    leukemia_doctor_1_regular_patients_total_processing_time = SimClasses.DTStat()
    leukemia_doctor_2_complex_patients_total_processing_time = SimClasses.DTStat()
    leukemia_doctor_2_regular_patients_total_processing_time = SimClasses.DTStat()
    transplant_doctor_1_complex_patients_total_processing_time = SimClasses.DTStat()
    transplant_doctor_1_regular_patients_total_processing_time = SimClasses.DTStat()
    transplant_doctor_2_complex_patients_total_processing_time = SimClasses.DTStat()
    transplant_doctor_2_regular_patients_total_processing_time = SimClasses.DTStat()
    transplant_doctor_3_complex_patients_total_processing_time = SimClasses.DTStat()
    transplant_doctor_3_regular_patients_total_processing_time = SimClasses.DTStat()
    other_patients_total_processing_time = SimClasses.DTStat()

    leukemia_doctor_1_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    leukemia_doctor_2_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    transplant_doctor_1_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    transplant_doctor_2_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    transplant_doctor_3_scheduled_vs_actual_time_diff = SimClasses.DTStat()

    nurse_station_1_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    nurse_station_2_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    nurse_station_3_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    nurse_station_4_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    nurse_station_5_scheduled_vs_actual_time_diff = SimClasses.DTStat()
    nurse_station_6_scheduled_vs_actual_time_diff = SimClasses.DTStat()

    q_flow_station_wait_time_avg = []
    q_flow_station_wait_time_var = []

    secretary_station_wait_time_avg = []
    secretary_station_wait_time_var = []

    nurse_station_1_wait_time_avg = []
    nurse_station_1_wait_time_var = []

    nurse_station_2_wait_time_avg = []
    nurse_station_2_wait_time_var = []

    nurse_station_3_wait_time_avg = []
    nurse_station_3_wait_time_var = []

    nurse_station_4_wait_time_avg = []
    nurse_station_4_wait_time_var = []

    nurse_station_5_wait_time_avg = []
    nurse_station_5_wait_time_var = []

    nurse_station_6_wait_time_avg = []
    nurse_station_6_wait_time_var = []

    leukemia_doctor_1_wait_time_avg = []
    leukemia_doctor_1_wait_time_var = []

    leukemia_doctor_2_wait_time_avg = []
    leukemia_doctor_2_wait_time_var = []

    transplant_doctor_1_wait_time_avg = []
    transplant_doctor_1_wait_time_var = []

    transplant_doctor_2_wait_time_avg = []
    transplant_doctor_2_wait_time_var = []

    transplant_doctor_3_wait_time_avg = []
    transplant_doctor_3_wait_time_var = []

    q_flow_station_queue_length_avg = []
    q_flow_station_queue_length_var = []

    secretary_station_queue_length_avg = []
    secretary_station_queue_length_var = []

    nurse_station_1_queue_length_avg = []
    nurse_station_1_queue_length_var = []

    nurse_station_2_queue_length_avg = []
    nurse_station_2_queue_length_var = []

    nurse_station_3_queue_length_avg = []
    nurse_station_3_queue_length_var = []

    nurse_station_4_queue_length_avg = []
    nurse_station_4_queue_length_var = []

    nurse_station_5_queue_length_avg = []
    nurse_station_5_queue_length_var = []

    nurse_station_6_queue_length_avg = []
    nurse_station_6_queue_length_var = []

    leukemia_doctor_1_queue_length_avg = []
    leukemia_doctor_1_queue_length_var = []

    leukemia_doctor_2_queue_length_avg = []
    leukemia_doctor_2_queue_length_var = []

    transplant_doctor_1_queue_length_avg = []
    transplant_doctor_1_queue_length_var = []

    transplant_doctor_2_queue_length_avg = []
    transplant_doctor_2_queue_length_var = []

    transplant_doctor_3_queue_length_avg = []
    transplant_doctor_3_queue_length_var = []

    q_flow_station_busy_avg = []
    q_flow_station_busy_var = []

    secretary_station_busy_avg = []
    secretary_station_busy_var = []

    nurse_station_1_busy_avg = []
    nurse_station_1_busy_var = []

    nurse_station_2_busy_avg = []
    nurse_station_2_busy_var = []

    nurse_station_3_busy_avg = []
    nurse_station_3_busy_var = []

    nurse_station_4_busy_avg = []
    nurse_station_4_busy_var = []

    nurse_station_5_busy_avg = []
    nurse_station_5_busy_var = []

    nurse_station_6_busy_avg = []
    nurse_station_6_busy_var = []

    leukemia_doctor_1_busy_avg = []
    leukemia_doctor_1_busy_var = []

    leukemia_doctor_2_busy_avg = []
    leukemia_doctor_2_busy_var = []

    transplant_doctor_1_busy_avg = []
    transplant_doctor_1_busy_var = []

    transplant_doctor_2_busy_avg = []  
    transplant_doctor_2_busy_var = []

    transplant_doctor_3_busy_avg = []
    transplant_doctor_3_busy_var = []

    q_flow_station_wait_time_var_avg = []
    q_flow_station_wait_time_var_var = []

    secretary_station_wait_time_var_avg = []
    secretary_station_wait_time_var_var = []

    q_flow_station_queue_length = []

    secretary_station_queue_length = []

    nurse_station_1_queue_length = []
    nurse_station_2_queue_length = []
    nurse_station_3_queue_length = []
    nurse_station_4_queue_length = []
    nurse_station_5_queue_length = []
    nurse_station_6_queue_length = []

    leukemia_doctor_1_queue_length = []
    leukemia_doctor_2_queue_length = []

    transplant_doctor_1_queue_length = []
    transplant_doctor_2_queue_length = []
    transplant_doctor_3_queue_length = []

    leukemia_doctor_1_complex_patients_total_processing_time_avg = []
    leukemia_doctor_1_regular_patients_total_processing_time_avg = []
    leukemia_doctor_1_complex_patients_total_processing_time_var = []
    leukemia_doctor_1_regular_patients_total_processing_time_var = []

    leukemia_doctor_2_complex_patients_total_processing_time_avg = []
    leukemia_doctor_2_regular_patients_total_processing_time_avg = []
    leukemia_doctor_2_complex_patients_total_processing_time_var = []
    leukemia_doctor_2_regular_patients_total_processing_time_var = []

    transplant_doctor_1_complex_patients_total_processing_time_avg = []
    transplant_doctor_1_regular_patients_total_processing_time_avg = []
    transplant_doctor_1_complex_patients_total_processing_time_var = []
    transplant_doctor_1_regular_patients_total_processing_time_var = []

    transplant_doctor_2_complex_patients_total_processing_time_avg = []
    transplant_doctor_2_regular_patients_total_processing_time_avg = []
    transplant_doctor_2_complex_patients_total_processing_time_var = []
    transplant_doctor_2_regular_patients_total_processing_time_var = []

    transplant_doctor_3_complex_patients_total_processing_time_avg = []
    transplant_doctor_3_regular_patients_total_processing_time_avg = []
    transplant_doctor_3_complex_patients_total_processing_time_var = []
    transplant_doctor_3_regular_patients_total_processing_time_var = []

    other_patients_total_processing_time_avg = []
    other_patients_total_processing_time_var = []

    leukemia_doctor_1_scheduled_vs_actual_time_diff_avg = []
    leukemia_doctor_2_scheduled_vs_actual_time_diff_avg = []
    transplant_doctor_1_scheduled_vs_actual_time_diff_avg = []
    transplant_doctor_2_scheduled_vs_actual_time_diff_avg = []
    transplant_doctor_3_scheduled_vs_actual_time_diff_avg = []

    leukemia_doctor_1_scheduled_vs_actual_time_diff_var = []
    leukemia_doctor_2_scheduled_vs_actual_time_diff_var = []
    transplant_doctor_1_scheduled_vs_actual_time_diff_var = []
    transplant_doctor_2_scheduled_vs_actual_time_diff_var = []
    transplant_doctor_3_scheduled_vs_actual_time_diff_var = []

    nurse_station_1_scheduled_vs_actual_time_diff_avg = []
    nurse_station_2_scheduled_vs_actual_time_diff_avg = []
    nurse_station_3_scheduled_vs_actual_time_diff_avg = []
    nurse_station_4_scheduled_vs_actual_time_diff_avg = []
    nurse_station_5_scheduled_vs_actual_time_diff_avg = []
    nurse_station_6_scheduled_vs_actual_time_diff_avg = []

    nurse_station_1_scheduled_vs_actual_time_diff_var = []
    nurse_station_2_scheduled_vs_actual_time_diff_var = []
    nurse_station_3_scheduled_vs_actual_time_diff_var = []
    nurse_station_4_scheduled_vs_actual_time_diff_var = []
    nurse_station_5_scheduled_vs_actual_time_diff_var = []
    nurse_station_6_scheduled_vs_actual_time_diff_var = []

    # Load cached patient profiles
    with open('../cached_patient_profiles.json', 'r') as f:
        cached_profiles = json.load(f)

    pbar_outer = tqdm(total=simulation_configuration.num_epochs, desc="Running Simulation")
    for epoch in range(simulation_configuration.num_epochs):
        SimFunctions.SimFunctionsInit(Calendar)
        
        # Use cached profile for this epoch
        profile = cached_profiles[epoch % len(cached_profiles)]
        list_of_patients = utils.generate_patients_from_profile(Calendar, model_parameters, profile)
        for patient_list in list_of_patients:
            for patient in patient_list:
                if patient.visits_nurse:
                    nurse_station = utils.assign_nurse_station_multi_queue(patient.get_type(), patient.complexity_level, model_parameters)
                    patient.set_nurse_name(nurse_station)

        nurse_num_patients = {"nurse_1": sum([utils.get_nurse_number_of_patients_multi_queue(patient_list, "nurse_station_1") for patient_list in list_of_patients]),
                            "nurse_2": sum([utils.get_nurse_number_of_patients_multi_queue(patient_list, "nurse_station_2") for patient_list in list_of_patients]),
                            "nurse_3": sum([utils.get_nurse_number_of_patients_multi_queue(patient_list, "nurse_station_3") for patient_list in list_of_patients]),
                            "nurse_4": sum([utils.get_nurse_number_of_patients_multi_queue(patient_list, "nurse_station_4") for patient_list in list_of_patients]),
                            "nurse_5": sum([utils.get_nurse_number_of_patients_multi_queue(patient_list, "nurse_station_5") for patient_list in list_of_patients]),
                            "nurse_6": sum([utils.get_nurse_number_of_patients_multi_queue(patient_list, "nurse_station_6") for patient_list in list_of_patients])}
        counters = {"nurse_1": 0, "nurse_2": 0, "nurse_3": 0, "nurse_4": 0, "nurse_5": 0, "nurse_6": 0}

        #schedule long service times for patients that visit nurse 6
        for patient_list in list_of_patients:
            for index, patient in enumerate(patient_list):
                nurse_station = patient.nurse_name
                if nurse_station == "nurse_station_6":
                    if index == len(patient_list) - 1:
                        utils.personalize_patient_schedule(patient, None, model_parameters)
                    else:
                        utils.personalize_patient_schedule(patient, patient_list[index + 1], model_parameters)
        if simulation_configuration.personalize_schedule:
            for patient_list in list_of_patients:
                for index, patient in enumerate(patient_list):
                    nurse_station = patient.nurse_name
                    if nurse_station != "nurse_station_6":
                        if index == len(patient_list) - 1:
                            utils.personalize_patient_schedule(patient, None, model_parameters)
                        else:
                            utils.personalize_patient_schedule(patient, patient_list[index + 1], model_parameters)
        
        doctors_start_service = False #Doctors only begin to see patients 150 minutes after the simulation starts (10:00 AM)
        schedule_start_time = 150
        utils.schedule_doctor_service_start_time(Calendar, schedule_start_time)
        
        while Calendar.N() > 0 and not utils.all_left_department(list_of_patients):
            NextEvent = Calendar.Remove()
            SimClasses.Clock = NextEvent.EventTime

            if NextEvent.EventType == "q_flow_station_start_of_waiting":
                q_flow_station_queue_length.append(q_flow_station_queue.NumQueue())
                utils.q_flow_station_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, q_flow_station_queue, q_flow_station, q_flow_station_wait_time, Calendar)
            
            elif NextEvent.EventType == "q_flow_station_service_start":
                utils.q_flow_station_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "q_flow_station_service_end":
                utils.q_flow_station_service_end(NextEvent.WhichObject, q_flow_station, q_flow_station_queue, q_flow_station_wait_time, Calendar)
            
            elif NextEvent.EventType == "secretary_station_start_of_waiting":
                secretary_station_queue_length.append(secretary_station_queue.NumQueue())
                utils.secretary_station_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, secretary_station_queue, secretary_station, secretary_station_wait_time, Calendar)
            
            elif NextEvent.EventType == "secretary_station_service_start":
                utils.secretary_station_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "secretary_station_service_end":
                
                utils.secretary_station_service_end(NextEvent.WhichObject, model_parameters, secretary_station, secretary_station_queue, secretary_station_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_1_start_of_waiting":
                nurse_station_1_queue_length.append(nurse_station_1_queue.NumQueue())
                utils.nurse_station_1_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, nurse_station_1_queue, nurse_station_1, nurse_station_1_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_1_service_start":
                utils.nurse_station_1_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "nurse_station_1_service_end":
                counters["nurse_1"] += 1
                if counters["nurse_1"] == nurse_num_patients["nurse_1"]:
                    nurse_station_1_busy_avg.append(nurse_station_1.Mean())
                    nurse_station_1_busy_var.append(nurse_station_1.Variance())
                utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
                utils.nurse_station_1_service_end(NextEvent.WhichObject, nurse_station_1, nurse_station_1_queue, nurse_station_1_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_2_start_of_waiting":
                nurse_station_2_queue_length.append(nurse_station_2_queue.NumQueue())
                utils.nurse_station_2_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, nurse_station_2_queue, nurse_station_2, nurse_station_2_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_2_service_start":
                utils.nurse_station_2_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "nurse_station_2_service_end":
                counters["nurse_2"] += 1
                if counters["nurse_2"] == nurse_num_patients["nurse_2"]:
                    nurse_station_2_busy_avg.append(nurse_station_2.Mean())  # Use actual busy time
                    nurse_station_2_busy_var.append(nurse_station_2.Variance())  # Use actual busy time variance
                utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
                utils.nurse_station_2_service_end(NextEvent.WhichObject, nurse_station_2, nurse_station_2_queue, nurse_station_2_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_3_start_of_waiting":
                nurse_station_3_queue_length.append(nurse_station_3_queue.NumQueue())
                utils.nurse_station_3_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, nurse_station_3_queue, nurse_station_3, nurse_station_3_wait_time, Calendar)   
            
            elif NextEvent.EventType == "nurse_station_3_service_start":
                utils.nurse_station_3_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "nurse_station_3_service_end":
                counters["nurse_3"] += 1
                if counters["nurse_3"] == nurse_num_patients["nurse_3"]:
                    nurse_station_3_busy_avg.append(nurse_station_3.Mean())  # Use actual busy time
                    nurse_station_3_busy_var.append(nurse_station_3.Variance())  # Use actual busy time variance
                utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
                utils.nurse_station_3_service_end(NextEvent.WhichObject, nurse_station_3, nurse_station_3_queue, nurse_station_3_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_4_start_of_waiting":
                nurse_station_4_queue_length.append(nurse_station_4_queue.NumQueue())
                utils.nurse_station_4_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, nurse_station_4_queue, nurse_station_4, nurse_station_4_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_4_service_start":
                utils.nurse_station_4_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "nurse_station_4_service_end":
                counters["nurse_4"] += 1
                if counters["nurse_4"] == nurse_num_patients["nurse_4"]:
                    nurse_station_4_busy_avg.append(nurse_station_4.Mean())  # Use actual busy time
                    nurse_station_4_busy_var.append(nurse_station_4.Variance())  # Use actual busy time variance
                utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
                utils.nurse_station_4_service_end(NextEvent.WhichObject, nurse_station_4, nurse_station_4_queue, nurse_station_4_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_5_start_of_waiting":
                nurse_station_5_queue_length.append(nurse_station_5_queue.NumQueue())
                utils.nurse_station_5_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, nurse_station_5_queue, nurse_station_5, nurse_station_5_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_5_service_start":
                utils.nurse_station_5_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "nurse_station_5_service_end":
                counters["nurse_5"] += 1
                if counters["nurse_5"] == nurse_num_patients["nurse_5"]:
                    nurse_station_5_busy_avg.append(nurse_station_5.Mean())  # Use actual busy time
                    nurse_station_5_busy_var.append(nurse_station_5.Variance())  # Use actual busy time variance
                utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
                utils.nurse_station_5_service_end(NextEvent.WhichObject, nurse_station_5, nurse_station_5_queue, nurse_station_5_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_6_start_of_waiting":
                nurse_station_6_queue_length.append(nurse_station_6_queue.NumQueue())
                utils.nurse_station_6_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, nurse_station_6_queue, nurse_station_6, nurse_station_6_wait_time, Calendar)
            
            elif NextEvent.EventType == "nurse_station_6_service_start":
                utils.nurse_station_6_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "nurse_station_6_service_end":
                counters["nurse_6"] += 1
                if counters["nurse_6"] == nurse_num_patients["nurse_6"]:
                    nurse_station_6_busy_avg.append(nurse_station_6.Mean())  # Use actual busy time
                    nurse_station_6_busy_var.append(nurse_station_6.Variance())  # Use actual busy time variance
                utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
                utils.nurse_station_6_service_end(NextEvent.WhichObject, nurse_station_6, nurse_station_6_queue, nurse_station_6_wait_time, Calendar)
            
            elif NextEvent.EventType == "receive_blood_test_results":
                NextEvent.WhichObject.receive_blood_test_results(SimClasses.Clock)
            
            elif NextEvent.EventType == "set_doctor_service_start_flag_to_true":
                doctors_start_service = True
                # Check each doctor's queue
                utils.check_doctor_queue_and_start_service(leukemia_doctor_1, leukemia_doctor_1_queue, leukemia_doctor_1_wait_time, Calendar, "leukemia_doctor_1")
                utils.check_doctor_queue_and_start_service(leukemia_doctor_2, leukemia_doctor_2_queue, leukemia_doctor_2_wait_time, Calendar, "leukemia_doctor_2")
                utils.check_doctor_queue_and_start_service(transplant_doctor_1, transplant_doctor_1_queue, transplant_doctor_1_wait_time, Calendar, "transplant_doctor_1")
                utils.check_doctor_queue_and_start_service(transplant_doctor_2, transplant_doctor_2_queue, transplant_doctor_2_wait_time, Calendar, "transplant_doctor_2")
                utils.check_doctor_queue_and_start_service(transplant_doctor_3, transplant_doctor_3_queue, transplant_doctor_3_wait_time, Calendar, "transplant_doctor_3")
            
            elif NextEvent.EventType == "leukemia_doctor_1_start_of_waiting":
                leukemia_doctor_1_queue_length.append(leukemia_doctor_1_queue.NumQueue())
                utils.leukemia_doctor_1_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, leukemia_doctor_1_queue, leukemia_doctor_1, leukemia_doctor_1_wait_time, Calendar, doctors_start_service)   

            elif NextEvent.EventType == "leukemia_doctor_1_service_start":
                utils.leukemia_doctor_1_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "leukemia_doctor_1_service_end":
                utils.leukemia_doctor_1_service_end(NextEvent.WhichObject, leukemia_doctor_1, leukemia_doctor_1_queue, leukemia_doctor_1_wait_time, Calendar)
            
            elif NextEvent.EventType == "leukemia_doctor_2_start_of_waiting":
                leukemia_doctor_2_queue_length.append(leukemia_doctor_2_queue.NumQueue())
                utils.leukemia_doctor_2_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, leukemia_doctor_2_queue, leukemia_doctor_2, leukemia_doctor_2_wait_time, Calendar, doctors_start_service)
            
            elif NextEvent.EventType == "leukemia_doctor_2_service_start":
                utils.leukemia_doctor_2_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "leukemia_doctor_2_service_end":
                utils.leukemia_doctor_2_service_end(NextEvent.WhichObject, leukemia_doctor_2, leukemia_doctor_2_queue, leukemia_doctor_2_wait_time, Calendar)
            
            elif NextEvent.EventType == "transplant_doctor_1_start_of_waiting":
                transplant_doctor_1_queue_length.append(transplant_doctor_1_queue.NumQueue())
                utils.transplant_doctor_1_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_doctor_1_queue, transplant_doctor_1, transplant_doctor_1_wait_time, Calendar, doctors_start_service)
            
            elif NextEvent.EventType == "transplant_doctor_1_service_start":
                utils.transplant_doctor_1_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "transplant_doctor_1_service_end":
                utils.transplant_doctor_1_service_end(NextEvent.WhichObject, transplant_doctor_1, transplant_doctor_1_queue, transplant_doctor_1_wait_time, Calendar)
            
            elif NextEvent.EventType == "transplant_doctor_2_start_of_waiting":
                transplant_doctor_2_queue_length.append(transplant_doctor_2_queue.NumQueue())
                utils.transplant_doctor_2_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_doctor_2_queue, transplant_doctor_2, transplant_doctor_2_wait_time, Calendar, doctors_start_service)
            
            elif NextEvent.EventType == "transplant_doctor_2_service_start":
                utils.transplant_doctor_2_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "transplant_doctor_2_service_end":
                utils.transplant_doctor_2_service_end(NextEvent.WhichObject, transplant_doctor_2, transplant_doctor_2_queue, transplant_doctor_2_wait_time, Calendar)
            
            elif NextEvent.EventType == "transplant_doctor_3_start_of_waiting":
                transplant_doctor_3_queue_length.append(transplant_doctor_3_queue.NumQueue())
                utils.transplant_doctor_3_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_doctor_3_queue, transplant_doctor_3, transplant_doctor_3_wait_time, Calendar, doctors_start_service)
            
            elif NextEvent.EventType == "transplant_doctor_3_service_start":
                utils.transplant_doctor_3_service_start(NextEvent.WhichObject, model_parameters, Calendar)
            
            elif NextEvent.EventType == "transplant_doctor_3_service_end":
                utils.transplant_doctor_3_service_end(NextEvent.WhichObject, transplant_doctor_3, transplant_doctor_3_queue, transplant_doctor_3_wait_time, Calendar)
            
            elif NextEvent.EventType == "process_complete" or NextEvent.EventType == "other_start_of_waiting" or NextEvent.EventType == "other_doctor_start_of_waiting":
                #here the process ends for the other patients
                utils.process_complete(NextEvent.WhichObject, SimClasses.Clock,
                                    nurse_station_1_scheduled_vs_actual_time_diff, nurse_station_2_scheduled_vs_actual_time_diff, nurse_station_3_scheduled_vs_actual_time_diff,
                                    nurse_station_4_scheduled_vs_actual_time_diff, nurse_station_5_scheduled_vs_actual_time_diff, nurse_station_6_scheduled_vs_actual_time_diff,
                                    leukemia_doctor_1_scheduled_vs_actual_time_diff, leukemia_doctor_1_complex_patients_total_processing_time, leukemia_doctor_1_regular_patients_total_processing_time,
                                    leukemia_doctor_2_scheduled_vs_actual_time_diff, leukemia_doctor_2_complex_patients_total_processing_time, leukemia_doctor_2_regular_patients_total_processing_time,
                                    transplant_doctor_1_scheduled_vs_actual_time_diff, transplant_doctor_1_complex_patients_total_processing_time, transplant_doctor_1_regular_patients_total_processing_time,
                                    transplant_doctor_2_scheduled_vs_actual_time_diff, transplant_doctor_2_complex_patients_total_processing_time, transplant_doctor_2_regular_patients_total_processing_time,
                                    transplant_doctor_3_scheduled_vs_actual_time_diff, transplant_doctor_3_complex_patients_total_processing_time, transplant_doctor_3_regular_patients_total_processing_time,
                                    other_patients_total_processing_time, Calendar)
            else:
                print(NextEvent.EventType)
                print("Unknown event type")
                raise ValueError(f"Unknown event type: {NextEvent.EventType}")
        #storing statistics from all DTStat objects
        q_flow_station_wait_time_avg.append(q_flow_station_wait_time.Mean())
        q_flow_station_wait_time_var.append(q_flow_station_wait_time.StdDev()**2)
        secretary_station_wait_time_avg.append(secretary_station_wait_time.Mean())
        secretary_station_wait_time_var.append(secretary_station_wait_time.StdDev()**2)
        nurse_station_1_wait_time_avg.append(nurse_station_1_wait_time.Mean())
        nurse_station_1_wait_time_var.append(nurse_station_1_wait_time.StdDev()**2)
        nurse_station_2_wait_time_avg.append(nurse_station_2_wait_time.Mean())
        nurse_station_2_wait_time_var.append(nurse_station_2_wait_time.StdDev()**2)
        nurse_station_3_wait_time_avg.append(nurse_station_3_wait_time.Mean())
        nurse_station_3_wait_time_var.append(nurse_station_3_wait_time.StdDev()**2)
        nurse_station_4_wait_time_avg.append(nurse_station_4_wait_time.Mean())
        nurse_station_4_wait_time_var.append(nurse_station_4_wait_time.StdDev()**2)
        nurse_station_5_wait_time_avg.append(nurse_station_5_wait_time.Mean())
        nurse_station_5_wait_time_var.append(nurse_station_5_wait_time.StdDev()**2)
        nurse_station_6_wait_time_avg.append(nurse_station_6_wait_time.Mean())
        nurse_station_6_wait_time_var.append(nurse_station_6_wait_time.StdDev()**2)
        leukemia_doctor_1_wait_time_avg.append(leukemia_doctor_1_wait_time.Mean())
        leukemia_doctor_1_wait_time_var.append(leukemia_doctor_1_wait_time.StdDev()**2)
        leukemia_doctor_2_wait_time_avg.append(leukemia_doctor_2_wait_time.Mean())
        leukemia_doctor_2_wait_time_var.append(leukemia_doctor_2_wait_time.StdDev()**2)
        transplant_doctor_1_wait_time_avg.append(transplant_doctor_1_wait_time.Mean())
        transplant_doctor_1_wait_time_var.append(transplant_doctor_1_wait_time.StdDev()**2)
        transplant_doctor_2_wait_time_avg.append(transplant_doctor_2_wait_time.Mean())
        transplant_doctor_2_wait_time_var.append(transplant_doctor_2_wait_time.StdDev()**2)
        transplant_doctor_3_wait_time_avg.append(transplant_doctor_3_wait_time.Mean())
        transplant_doctor_3_wait_time_var.append(transplant_doctor_3_wait_time.StdDev()**2)

        leukemia_doctor_1_complex_patients_total_processing_time_avg.append(leukemia_doctor_1_complex_patients_total_processing_time.Mean())
        leukemia_doctor_1_regular_patients_total_processing_time_avg.append(leukemia_doctor_1_regular_patients_total_processing_time.Mean())
        leukemia_doctor_1_complex_patients_total_processing_time_var.append(leukemia_doctor_1_complex_patients_total_processing_time.StdDev()**2)
        leukemia_doctor_1_regular_patients_total_processing_time_var.append(leukemia_doctor_1_regular_patients_total_processing_time.StdDev()**2)
        leukemia_doctor_2_complex_patients_total_processing_time_avg.append(leukemia_doctor_2_complex_patients_total_processing_time.Mean())
        leukemia_doctor_2_regular_patients_total_processing_time_avg.append(leukemia_doctor_2_regular_patients_total_processing_time.Mean())
        leukemia_doctor_2_complex_patients_total_processing_time_var.append(leukemia_doctor_2_complex_patients_total_processing_time.StdDev()**2)
        leukemia_doctor_2_regular_patients_total_processing_time_var.append(leukemia_doctor_2_regular_patients_total_processing_time.StdDev()**2)
        transplant_doctor_1_complex_patients_total_processing_time_avg.append(transplant_doctor_1_complex_patients_total_processing_time.Mean())
        transplant_doctor_1_regular_patients_total_processing_time_avg.append(transplant_doctor_1_regular_patients_total_processing_time.Mean())
        transplant_doctor_1_complex_patients_total_processing_time_var.append(transplant_doctor_1_complex_patients_total_processing_time.StdDev()**2)
        transplant_doctor_1_regular_patients_total_processing_time_var.append(transplant_doctor_1_regular_patients_total_processing_time.StdDev()**2)
        transplant_doctor_2_complex_patients_total_processing_time_avg.append(transplant_doctor_2_complex_patients_total_processing_time.Mean())
        transplant_doctor_2_regular_patients_total_processing_time_avg.append(transplant_doctor_2_regular_patients_total_processing_time.Mean())
        transplant_doctor_2_complex_patients_total_processing_time_var.append(transplant_doctor_2_complex_patients_total_processing_time.StdDev()**2)
        transplant_doctor_2_regular_patients_total_processing_time_var.append(transplant_doctor_2_regular_patients_total_processing_time.StdDev()**2)
        transplant_doctor_3_complex_patients_total_processing_time_avg.append(transplant_doctor_3_complex_patients_total_processing_time.Mean())
        transplant_doctor_3_regular_patients_total_processing_time_avg.append(transplant_doctor_3_regular_patients_total_processing_time.Mean())
        transplant_doctor_3_complex_patients_total_processing_time_var.append(transplant_doctor_3_complex_patients_total_processing_time.StdDev()**2)
        transplant_doctor_3_regular_patients_total_processing_time_var.append(transplant_doctor_3_regular_patients_total_processing_time.StdDev()**2)
        other_patients_total_processing_time_avg.append(other_patients_total_processing_time.Mean())
        other_patients_total_processing_time_var.append(other_patients_total_processing_time.StdDev()**2)

        q_flow_station_queue_length_avg.append(q_flow_station_queue.Mean())
        q_flow_station_queue_length_var.append(q_flow_station_queue.Variance())
        secretary_station_queue_length_avg.append(secretary_station_queue.Mean())
        secretary_station_queue_length_var.append(secretary_station_queue.Variance())
        nurse_station_1_queue_length_avg.append(nurse_station_1_queue.Mean())
        nurse_station_1_queue_length_var.append(nurse_station_1_queue.Variance())
        nurse_station_2_queue_length_avg.append(nurse_station_2_queue.Mean())
        nurse_station_2_queue_length_var.append(nurse_station_2_queue.Variance())
        nurse_station_3_queue_length_avg.append(nurse_station_3_queue.Mean())
        nurse_station_3_queue_length_var.append(nurse_station_3_queue.Variance())
        nurse_station_4_queue_length_avg.append(nurse_station_4_queue.Mean())
        nurse_station_4_queue_length_var.append(nurse_station_4_queue.Variance())
        nurse_station_5_queue_length_avg.append(nurse_station_5_queue.Mean())
        nurse_station_5_queue_length_var.append(nurse_station_5_queue.Variance())
        nurse_station_6_queue_length_avg.append(nurse_station_6_queue.Mean())
        nurse_station_6_queue_length_var.append(nurse_station_6_queue.Variance())
        leukemia_doctor_1_queue_length_avg.append(leukemia_doctor_1_queue.Mean())
        leukemia_doctor_1_queue_length_var.append(leukemia_doctor_1_queue.Variance())
        leukemia_doctor_2_queue_length_avg.append(leukemia_doctor_2_queue.Mean())
        leukemia_doctor_2_queue_length_var.append(leukemia_doctor_2_queue.Variance())
        transplant_doctor_1_queue_length_avg.append(transplant_doctor_1_queue.Mean())
        transplant_doctor_1_queue_length_var.append(transplant_doctor_1_queue.Variance())
        transplant_doctor_2_queue_length_avg.append(transplant_doctor_2_queue.Mean())
        transplant_doctor_2_queue_length_var.append(transplant_doctor_2_queue.Variance())
        transplant_doctor_3_queue_length_avg.append(transplant_doctor_3_queue.Mean())
        transplant_doctor_3_queue_length_var.append(transplant_doctor_3_queue.Variance())

        q_flow_station_busy_avg.append(q_flow_station.Mean())
        q_flow_station_busy_var.append(q_flow_station.Variance())
        secretary_station_busy_avg.append(secretary_station.Mean())
        secretary_station_busy_var.append(secretary_station.Variance())
        leukemia_doctor_1_busy_avg.append(leukemia_doctor_1.Mean())
        leukemia_doctor_1_busy_var.append(leukemia_doctor_1.Variance())
        leukemia_doctor_2_busy_avg.append(leukemia_doctor_2.Mean())
        leukemia_doctor_2_busy_var.append(leukemia_doctor_2.Variance())
        transplant_doctor_1_busy_avg.append(transplant_doctor_1.Mean())
        transplant_doctor_1_busy_var.append(transplant_doctor_1.Variance())
        transplant_doctor_2_busy_avg.append(transplant_doctor_2.Mean())
        transplant_doctor_2_busy_var.append(transplant_doctor_2.Variance())
        transplant_doctor_3_busy_avg.append(transplant_doctor_3.Mean())
        transplant_doctor_3_busy_var.append(transplant_doctor_3.Variance())

        leukemia_doctor_1_scheduled_vs_actual_time_diff_avg.append(leukemia_doctor_1_scheduled_vs_actual_time_diff.Mean())
        leukemia_doctor_2_scheduled_vs_actual_time_diff_avg.append(leukemia_doctor_2_scheduled_vs_actual_time_diff.Mean())
        transplant_doctor_1_scheduled_vs_actual_time_diff_avg.append(transplant_doctor_1_scheduled_vs_actual_time_diff.Mean())
        transplant_doctor_2_scheduled_vs_actual_time_diff_avg.append(transplant_doctor_2_scheduled_vs_actual_time_diff.Mean())
        transplant_doctor_3_scheduled_vs_actual_time_diff_avg.append(transplant_doctor_3_scheduled_vs_actual_time_diff.Mean())

        leukemia_doctor_1_scheduled_vs_actual_time_diff_var.append(leukemia_doctor_1_scheduled_vs_actual_time_diff.StdDev()**2)
        leukemia_doctor_2_scheduled_vs_actual_time_diff_var.append(leukemia_doctor_2_scheduled_vs_actual_time_diff.StdDev()**2)
        transplant_doctor_1_scheduled_vs_actual_time_diff_var.append(transplant_doctor_1_scheduled_vs_actual_time_diff.StdDev()**2)
        transplant_doctor_2_scheduled_vs_actual_time_diff_var.append(transplant_doctor_2_scheduled_vs_actual_time_diff.StdDev()**2)
        transplant_doctor_3_scheduled_vs_actual_time_diff_var.append(transplant_doctor_3_scheduled_vs_actual_time_diff.StdDev()**2)

        nurse_station_1_scheduled_vs_actual_time_diff_avg.append(nurse_station_1_scheduled_vs_actual_time_diff.Mean())
        nurse_station_2_scheduled_vs_actual_time_diff_avg.append(nurse_station_2_scheduled_vs_actual_time_diff.Mean())
        nurse_station_3_scheduled_vs_actual_time_diff_avg.append(nurse_station_3_scheduled_vs_actual_time_diff.Mean())
        nurse_station_4_scheduled_vs_actual_time_diff_avg.append(nurse_station_4_scheduled_vs_actual_time_diff.Mean())
        nurse_station_5_scheduled_vs_actual_time_diff_avg.append(nurse_station_5_scheduled_vs_actual_time_diff.Mean())
        nurse_station_6_scheduled_vs_actual_time_diff_avg.append(nurse_station_6_scheduled_vs_actual_time_diff.Mean())

        nurse_station_1_scheduled_vs_actual_time_diff_var.append(nurse_station_1_scheduled_vs_actual_time_diff.StdDev()**2)
        nurse_station_2_scheduled_vs_actual_time_diff_var.append(nurse_station_2_scheduled_vs_actual_time_diff.StdDev()**2)
        nurse_station_3_scheduled_vs_actual_time_diff_var.append(nurse_station_3_scheduled_vs_actual_time_diff.StdDev()**2)
        nurse_station_4_scheduled_vs_actual_time_diff_var.append(nurse_station_4_scheduled_vs_actual_time_diff.StdDev()**2)
        nurse_station_5_scheduled_vs_actual_time_diff_var.append(nurse_station_5_scheduled_vs_actual_time_diff.StdDev()**2)
        nurse_station_6_scheduled_vs_actual_time_diff_var.append(nurse_station_6_scheduled_vs_actual_time_diff.StdDev()**2)

        if epoch == 0:
            if simulation_configuration.personalize_schedule:
                utils.generate_patient_attributes_csv(list_of_patients, "results_directory/same_patient_profiles/multi_queue_v2/personalized/patient_attributes.csv")
            else:
                utils.generate_patient_attributes_csv(list_of_patients, "results_directory/same_patient_profiles/multi_queue_v2/current_state/patient_attributes.csv")

        pbar_outer.set_description(f"Running Simulation - {epoch+1}/{simulation_configuration.num_epochs}")

        pbar_outer.update(1)

    pbar_outer.close()
    print("Simulation completed")

    print("Array Lengths:")
    print(f"q_flow_station_wait_time_avg: {len(q_flow_station_wait_time_avg)}")
    print(f"q_flow_station_queue_length_avg: {len(q_flow_station_queue_length_avg)}")
    print(f"q_flow_station_busy_avg: {len(q_flow_station_busy_avg)}")
    print(f"secretary_station_wait_time_avg: {len(secretary_station_wait_time_avg)}")
    print(f"secretary_station_queue_length_avg: {len(secretary_station_queue_length_avg)}")
    print(f"secretary_station_busy_avg: {len(secretary_station_busy_avg)}")
    print(f"nurse_station_1_wait_time_avg: {len(nurse_station_1_wait_time_avg)}")
    print(f"nurse_station_1_queue_length_avg: {len(nurse_station_1_queue_length_avg)}")
    print(f"nurse_station_1_busy_avg: {len(nurse_station_1_busy_avg)}")
    print(f"nurse_station_2_wait_time_avg: {len(nurse_station_2_wait_time_avg)}")
    print(f"nurse_station_2_queue_length_avg: {len(nurse_station_2_queue_length_avg)}")
    print(f"nurse_station_2_busy_avg: {len(nurse_station_2_busy_avg)}")
    print(f"nurse_station_3_wait_time_avg: {len(nurse_station_3_wait_time_avg)}")
    print(f"nurse_station_3_queue_length_avg: {len(nurse_station_3_queue_length_avg)}")
    print(f"nurse_station_3_busy_avg: {len(nurse_station_3_busy_avg)}")
    print(f"nurse_station_4_wait_time_avg: {len(nurse_station_4_wait_time_avg)}")
    print(f"nurse_station_4_queue_length_avg: {len(nurse_station_4_queue_length_avg)}")
    print(f"nurse_station_4_busy_avg: {len(nurse_station_4_busy_avg)}")
    print(f"nurse_station_5_wait_time_avg: {len(nurse_station_5_wait_time_avg)}")
    print(f"nurse_station_5_queue_length_avg: {len(nurse_station_5_queue_length_avg)}")
    print(f"nurse_station_5_busy_avg: {len(nurse_station_5_busy_avg)}")
    print(f"nurse_station_6_wait_time_avg: {len(nurse_station_6_wait_time_avg)}")
    print(f"nurse_station_6_queue_length_avg: {len(nurse_station_6_queue_length_avg)}")
    print(f"nurse_station_6_busy_avg: {len(nurse_station_6_busy_avg)}")
    print(f"leukemia_doctor_1_wait_time_avg: {len(leukemia_doctor_1_wait_time_avg)}")
    print(f"leukemia_doctor_1_queue_length_avg: {len(leukemia_doctor_1_queue_length_avg)}")
    print(f"leukemia_doctor_1_busy_avg: {len(leukemia_doctor_1_busy_avg)}")
    print(f"leukemia_doctor_2_wait_time_avg: {len(leukemia_doctor_2_wait_time_avg)}")
    print(f"leukemia_doctor_2_queue_length_avg: {len(leukemia_doctor_2_queue_length_avg)}")
    print(f"leukemia_doctor_2_busy_avg: {len(leukemia_doctor_2_busy_avg)}")
    print(f"transplant_doctor_1_wait_time_avg: {len(transplant_doctor_1_wait_time_avg)}")
    print(f"transplant_doctor_1_queue_length_avg: {len(transplant_doctor_1_queue_length_avg)}")
    print(f"transplant_doctor_1_busy_avg: {len(transplant_doctor_1_busy_avg)}")
    print(f"transplant_doctor_2_wait_time_avg: {len(transplant_doctor_2_wait_time_avg)}")
    print(f"transplant_doctor_2_queue_length_avg: {len(transplant_doctor_2_queue_length_avg)}")
    print(f"transplant_doctor_2_busy_avg: {len(transplant_doctor_2_busy_avg)}")
    print(f"transplant_doctor_3_wait_time_avg: {len(transplant_doctor_3_wait_time_avg)}")
    print(f"transplant_doctor_3_queue_length_avg: {len(transplant_doctor_3_queue_length_avg)}")
    print(f"transplant_doctor_3_busy_avg: {len(transplant_doctor_3_busy_avg)}")
    print(f"other_patients_total_processing_time_avg: {len(other_patients_total_processing_time_avg)}")
    print(f"leukemia_doctor_1_complex_patients_total_processing_time_avg: {len(leukemia_doctor_1_complex_patients_total_processing_time_avg)}")
    print(f"leukemia_doctor_1_regular_patients_total_processing_time_avg: {len(leukemia_doctor_1_regular_patients_total_processing_time_avg)}")
    print(f"leukemia_doctor_2_complex_patients_total_processing_time_avg: {len(leukemia_doctor_2_complex_patients_total_processing_time_avg)}")
    print(f"leukemia_doctor_2_regular_patients_total_processing_time_avg: {len(leukemia_doctor_2_regular_patients_total_processing_time_avg)}")
    print(f"transplant_doctor_1_complex_patients_total_processing_time_avg: {len(transplant_doctor_1_complex_patients_total_processing_time_avg)}")
    print(f"transplant_doctor_1_regular_patients_total_processing_time_avg: {len(transplant_doctor_1_regular_patients_total_processing_time_avg)}")
    print(f"transplant_doctor_2_complex_patients_total_processing_time_avg: {len(transplant_doctor_2_complex_patients_total_processing_time_avg)}")
    print(f"transplant_doctor_2_regular_patients_total_processing_time_avg: {len(transplant_doctor_2_regular_patients_total_processing_time_avg)}")
    print(f"transplant_doctor_3_complex_patients_total_processing_time_avg: {len(transplant_doctor_3_complex_patients_total_processing_time_avg)}")
    print(f"transplant_doctor_3_regular_patients_total_processing_time_avg: {len(transplant_doctor_3_regular_patients_total_processing_time_avg)}")
    print(f"leukemia_doctor_1_scheduled_vs_actual_time_diff_avg: {len(leukemia_doctor_1_scheduled_vs_actual_time_diff_avg)}")
    print(f"leukemia_doctor_2_scheduled_vs_actual_time_diff_avg: {len(leukemia_doctor_2_scheduled_vs_actual_time_diff_avg)}")
    print(f"transplant_doctor_1_scheduled_vs_actual_time_diff_avg: {len(transplant_doctor_1_scheduled_vs_actual_time_diff_avg)}")
    print(f"transplant_doctor_2_scheduled_vs_actual_time_diff_avg: {len(transplant_doctor_2_scheduled_vs_actual_time_diff_avg)}")
    print(f"transplant_doctor_3_scheduled_vs_actual_time_diff_avg: {len(transplant_doctor_3_scheduled_vs_actual_time_diff_avg)}")
    print(f"nurse_station_1_scheduled_vs_actual_time_diff_avg: {len(nurse_station_1_scheduled_vs_actual_time_diff_avg)}")
    print(f"nurse_station_2_scheduled_vs_actual_time_diff_avg: {len(nurse_station_2_scheduled_vs_actual_time_diff_avg)}")
    print(f"nurse_station_3_scheduled_vs_actual_time_diff_avg: {len(nurse_station_3_scheduled_vs_actual_time_diff_avg)}")
    print(f"nurse_station_4_scheduled_vs_actual_time_diff_avg: {len(nurse_station_4_scheduled_vs_actual_time_diff_avg)}")
    print(f"nurse_station_5_scheduled_vs_actual_time_diff_avg: {len(nurse_station_5_scheduled_vs_actual_time_diff_avg)}")
    print(f"nurse_station_6_scheduled_vs_actual_time_diff_avg: {len(nurse_station_6_scheduled_vs_actual_time_diff_avg)}")
    print("**********************************************************************************")

    averages_df = pd.DataFrame({
        "q_flow_station_wait_time_avg": q_flow_station_wait_time_avg,
        "q_flow_station_queue_length_avg": q_flow_station_queue_length_avg,
        "q_flow_station_busy_avg": q_flow_station_busy_avg,
        "secretary_station_wait_time_avg": secretary_station_wait_time_avg,
        "secretary_station_queue_length_avg": secretary_station_queue_length_avg,
        "secretary_station_busy_avg": secretary_station_busy_avg,
        "nurse_station_1_wait_time_avg": nurse_station_1_wait_time_avg,
        "nurse_station_1_queue_length_avg": nurse_station_1_queue_length_avg,
        "nurse_station_1_busy_avg": nurse_station_1_busy_avg,
        "nurse_station_2_wait_time_avg": nurse_station_2_wait_time_avg,
        "nurse_station_2_queue_length_avg": nurse_station_2_queue_length_avg,
        "nurse_station_2_busy_avg": nurse_station_2_busy_avg,
        "nurse_station_3_wait_time_avg": nurse_station_3_wait_time_avg,
        "nurse_station_3_queue_length_avg": nurse_station_3_queue_length_avg,
        "nurse_station_3_busy_avg": nurse_station_3_busy_avg,
        "nurse_station_4_wait_time_avg": nurse_station_4_wait_time_avg,
        "nurse_station_4_queue_length_avg": nurse_station_4_queue_length_avg,
        "nurse_station_4_busy_avg": nurse_station_4_busy_avg,
        "nurse_station_5_wait_time_avg": nurse_station_5_wait_time_avg,
        "nurse_station_5_queue_length_avg": nurse_station_5_queue_length_avg,
        "nurse_station_5_busy_avg": nurse_station_5_busy_avg,
        "nurse_station_6_wait_time_avg": nurse_station_6_wait_time_avg,
        "nurse_station_6_queue_length_avg": nurse_station_6_queue_length_avg,
        "nurse_station_6_busy_avg": nurse_station_6_busy_avg,
        "leukemia_doctor_1_wait_time_avg": leukemia_doctor_1_wait_time_avg,
        "leukemia_doctor_1_queue_length_avg": leukemia_doctor_1_queue_length_avg,
        "leukemia_doctor_1_busy_avg": leukemia_doctor_1_busy_avg,
        "leukemia_doctor_2_wait_time_avg": leukemia_doctor_2_wait_time_avg,
        "leukemia_doctor_2_queue_length_avg": leukemia_doctor_2_queue_length_avg,
        "leukemia_doctor_2_busy_avg": leukemia_doctor_2_busy_avg,
        "transplant_doctor_1_wait_time_avg": transplant_doctor_1_wait_time_avg,
        "transplant_doctor_1_queue_length_avg": transplant_doctor_1_queue_length_avg,
        "transplant_doctor_1_busy_avg": transplant_doctor_1_busy_avg,
        "transplant_doctor_2_wait_time_avg": transplant_doctor_2_wait_time_avg,
        "transplant_doctor_2_queue_length_avg": transplant_doctor_2_queue_length_avg,
        "transplant_doctor_2_busy_avg": transplant_doctor_2_busy_avg,
        "transplant_doctor_3_wait_time_avg": transplant_doctor_3_wait_time_avg,
        "transplant_doctor_3_queue_length_avg": transplant_doctor_3_queue_length_avg,
        "transplant_doctor_3_busy_avg": transplant_doctor_3_busy_avg,
        "other_patients_total_processing_time_avg": other_patients_total_processing_time_avg,
        "leukemia_doctor_1_complex_patients_total_processing_time_avg": leukemia_doctor_1_complex_patients_total_processing_time_avg,
        "leukemia_doctor_1_regular_patients_total_processing_time_avg": leukemia_doctor_1_regular_patients_total_processing_time_avg,
        "leukemia_doctor_2_complex_patients_total_processing_time_avg": leukemia_doctor_2_complex_patients_total_processing_time_avg,
        "leukemia_doctor_2_regular_patients_total_processing_time_avg": leukemia_doctor_2_regular_patients_total_processing_time_avg,
        "transplant_doctor_1_complex_patients_total_processing_time_avg": transplant_doctor_1_complex_patients_total_processing_time_avg,
        "transplant_doctor_1_regular_patients_total_processing_time_avg": transplant_doctor_1_regular_patients_total_processing_time_avg,
        "transplant_doctor_2_complex_patients_total_processing_time_avg": transplant_doctor_2_complex_patients_total_processing_time_avg,
        "transplant_doctor_2_regular_patients_total_processing_time_avg": transplant_doctor_2_regular_patients_total_processing_time_avg,
        "transplant_doctor_3_complex_patients_total_processing_time_avg": transplant_doctor_3_complex_patients_total_processing_time_avg,
        "transplant_doctor_3_regular_patients_total_processing_time_avg": transplant_doctor_3_regular_patients_total_processing_time_avg,
        "leukemia_doctor_1_scheduled_vs_actual_time_diff_avg": leukemia_doctor_1_scheduled_vs_actual_time_diff_avg,
        "leukemia_doctor_2_scheduled_vs_actual_time_diff_avg": leukemia_doctor_2_scheduled_vs_actual_time_diff_avg,
        "transplant_doctor_1_scheduled_vs_actual_time_diff_avg": transplant_doctor_1_scheduled_vs_actual_time_diff_avg,
        "transplant_doctor_2_scheduled_vs_actual_time_diff_avg": transplant_doctor_2_scheduled_vs_actual_time_diff_avg,
        "transplant_doctor_3_scheduled_vs_actual_time_diff_avg": transplant_doctor_3_scheduled_vs_actual_time_diff_avg,
        "nurse_station_1_scheduled_vs_actual_time_diff_avg": nurse_station_1_scheduled_vs_actual_time_diff_avg,
        "nurse_station_2_scheduled_vs_actual_time_diff_avg": nurse_station_2_scheduled_vs_actual_time_diff_avg,
        "nurse_station_3_scheduled_vs_actual_time_diff_avg": nurse_station_3_scheduled_vs_actual_time_diff_avg,
        "nurse_station_4_scheduled_vs_actual_time_diff_avg": nurse_station_4_scheduled_vs_actual_time_diff_avg,
        "nurse_station_5_scheduled_vs_actual_time_diff_avg": nurse_station_5_scheduled_vs_actual_time_diff_avg,
        "nurse_station_6_scheduled_vs_actual_time_diff_avg": nurse_station_6_scheduled_vs_actual_time_diff_avg
        })

    os.makedirs("results_directory/same_patient_profiles/multi_queue", exist_ok=True)
    if simulation_configuration.personalize_schedule:
        averages_df.to_csv(f"results_directory/same_patient_profiles/multi_queue_v2/personalized/averages_data.csv")
        print(f"Simulation Results Saved to results_directory/same_patient_profiles/multi_queue_v2/personalized/averages_data.csv")
    else:
        averages_df.to_csv(f"results_directory/same_patient_profiles/multi_queue_v2/current_state/averages_data.csv")
        print(f"Simulation Results Saved to results_directory/same_patient_profiles/multi_queue_v2/current_state/averages_data.csv")
    print("**********************************************************************************")
    print("Means of the simulation results:")
    print(averages_df.mean())
    print("**********************************************************************************")
    print("99% Confidence Intervals Half-Width")
    CI= scs.t.ppf(1-0.01/2, len(averages_df)-1)*np.sqrt(averages_df.var()/len(averages_df))
    print(CI)
    print("**********************************************************************************")
    print("Error:")
    print(CI/averages_df.mean())
    print("**********************************************************************************")
    print("Number of epochs required for 99% confidence, half-width 5 minutes for all measures:")
    print(max((scs.t.ppf(1-0.01, len(averages_df)-1)*np.sqrt(averages_df.var()/len(averages_df))/5)**2))
    print("Number of epochs required for 99% confidence, half-width 10 minutes for all measures:")
    print(max((scs.t.ppf(1-0.01/2, len(averages_df)-1)*np.sqrt(averages_df.var()/len(averages_df))/10)**2))

    variances_df = pd.DataFrame({
        "q_flow_station_wait_time_var": q_flow_station_wait_time_var,
        "q_flow_station_queue_length_var": q_flow_station_queue_length_var,
        "q_flow_station_busy_var": q_flow_station_busy_var,
        "secretary_station_wait_time_var": secretary_station_wait_time_var,
        "secretary_station_queue_length_var": secretary_station_queue_length_var,
        "secretary_station_busy_var": secretary_station_busy_var,
        "nurse_station_1_wait_time_var": nurse_station_1_wait_time_var,
        "nurse_station_1_queue_length_var": nurse_station_1_queue_length_var,
        "nurse_station_1_busy_var": nurse_station_1_busy_var,
        "nurse_station_2_wait_time_var": nurse_station_2_wait_time_var,
        "nurse_station_2_queue_length_var": nurse_station_2_queue_length_var,
        "nurse_station_2_busy_var": nurse_station_2_busy_var,
        "nurse_station_3_wait_time_var": nurse_station_3_wait_time_var,
        "nurse_station_3_queue_length_var": nurse_station_3_queue_length_var,
        "nurse_station_3_busy_var": nurse_station_3_busy_var,
        "nurse_station_4_wait_time_var": nurse_station_4_wait_time_var,
        "nurse_station_4_queue_length_var": nurse_station_4_queue_length_var,
        "nurse_station_4_busy_var": nurse_station_4_busy_var,
        "nurse_station_5_wait_time_var": nurse_station_5_wait_time_var,
        "nurse_station_5_queue_length_var": nurse_station_5_queue_length_var,
        "nurse_station_5_busy_var": nurse_station_5_busy_var,
        "nurse_station_6_wait_time_var": nurse_station_6_wait_time_var,
        "nurse_station_6_queue_length_var": nurse_station_6_queue_length_var,
        "nurse_station_6_busy_var": nurse_station_6_busy_var,
        "leukemia_doctor_1_wait_time_var": leukemia_doctor_1_wait_time_var,
        "leukemia_doctor_1_queue_length_var": leukemia_doctor_1_queue_length_var,
        "leukemia_doctor_1_busy_var": leukemia_doctor_1_busy_var,
        "leukemia_doctor_2_wait_time_var": leukemia_doctor_2_wait_time_var,
        "leukemia_doctor_2_queue_length_var": leukemia_doctor_2_queue_length_var,
        "leukemia_doctor_2_busy_var": leukemia_doctor_2_busy_var,
        "transplant_doctor_1_wait_time_var": transplant_doctor_1_wait_time_var,
        "transplant_doctor_1_queue_length_var": transplant_doctor_1_queue_length_var,
        "transplant_doctor_1_busy_var": transplant_doctor_1_busy_var,
        "transplant_doctor_2_wait_time_var": transplant_doctor_2_wait_time_var,
        "transplant_doctor_2_queue_length_var": transplant_doctor_2_queue_length_var,
        "transplant_doctor_2_busy_var": transplant_doctor_2_busy_var,
        "transplant_doctor_3_wait_time_var": transplant_doctor_3_wait_time_var,
        "transplant_doctor_3_queue_length_var": transplant_doctor_3_queue_length_var,
        "transplant_doctor_3_busy_var": transplant_doctor_3_busy_var,
        "other_patients_total_processing_time_var": other_patients_total_processing_time_var,
        "leukemia_doctor_1_complex_patients_total_processing_time_var": leukemia_doctor_1_complex_patients_total_processing_time_var,
        "leukemia_doctor_1_regular_patients_total_processing_time_var": leukemia_doctor_1_regular_patients_total_processing_time_var,
        "leukemia_doctor_2_complex_patients_total_processing_time_var": leukemia_doctor_2_complex_patients_total_processing_time_var,
        "leukemia_doctor_2_regular_patients_total_processing_time_var": leukemia_doctor_2_regular_patients_total_processing_time_var,
        "transplant_doctor_1_complex_patients_total_processing_time_var": transplant_doctor_1_complex_patients_total_processing_time_var,
        "transplant_doctor_1_regular_patients_total_processing_time_var": transplant_doctor_1_regular_patients_total_processing_time_var,
        "transplant_doctor_2_complex_patients_total_processing_time_var": transplant_doctor_2_complex_patients_total_processing_time_var,
        "transplant_doctor_2_regular_patients_total_processing_time_var": transplant_doctor_2_regular_patients_total_processing_time_var,
        "transplant_doctor_3_complex_patients_total_processing_time_var": transplant_doctor_3_complex_patients_total_processing_time_var,
        "transplant_doctor_3_regular_patients_total_processing_time_var": transplant_doctor_3_regular_patients_total_processing_time_var,
        "leukemia_doctor_1_scheduled_vs_actual_time_diff_var": leukemia_doctor_1_scheduled_vs_actual_time_diff_var,
        "leukemia_doctor_2_scheduled_vs_actual_time_diff_var": leukemia_doctor_2_scheduled_vs_actual_time_diff_var,
        "transplant_doctor_1_scheduled_vs_actual_time_diff_var": transplant_doctor_1_scheduled_vs_actual_time_diff_var,
        "transplant_doctor_2_scheduled_vs_actual_time_diff_var": transplant_doctor_2_scheduled_vs_actual_time_diff_var,
        "transplant_doctor_3_scheduled_vs_actual_time_diff_var": transplant_doctor_3_scheduled_vs_actual_time_diff_var,
        "nurse_station_1_scheduled_vs_actual_time_diff_var": nurse_station_1_scheduled_vs_actual_time_diff_var,
        "nurse_station_2_scheduled_vs_actual_time_diff_var": nurse_station_2_scheduled_vs_actual_time_diff_var,
        "nurse_station_3_scheduled_vs_actual_time_diff_var": nurse_station_3_scheduled_vs_actual_time_diff_var,
        "nurse_station_4_scheduled_vs_actual_time_diff_var": nurse_station_4_scheduled_vs_actual_time_diff_var,
        "nurse_station_5_scheduled_vs_actual_time_diff_var": nurse_station_5_scheduled_vs_actual_time_diff_var,
        "nurse_station_6_scheduled_vs_actual_time_diff_var": nurse_station_6_scheduled_vs_actual_time_diff_var
    })

    os.makedirs("results_directory/same_patient_profiles/multi_queue", exist_ok=True)
    if simulation_configuration.personalize_schedule:
        variances_df.to_csv(f"results_directory/same_patient_profiles/multi_queue_v2/personalized/variances_data.csv")
        print("Simulation Variance Results Saved to results_directory/same_patient_profiles/multi_queue_v2/personalized/variances_data.csv")
    else:
        variances_df.to_csv(f"results_directory/same_patient_profiles/multi_queue_v2/current_state/variances_data.csv")
        print("Simulation Variance Results Saved to results_directory/same_patient_profiles/multi_queue_v2/current_state/variances_data.csv")
    print("**********************************************************************************")

    # Number of epochs
    n = len(variances_df)
    alpha = 0.01  # 99% CI

    # Mean of the variances across epochs
    variance_means = variances_df.mean()
    print("Mean Variance of the simulation results:")
    print(variance_means)
    print("**********************************************************************************")

    # Chi-squared critical values
    chi2_lower = scs.chi2.ppf(1 - alpha / 2, df=n - 1)
    chi2_upper = scs.chi2.ppf(alpha / 2, df=n - 1)

    # Confidence interval half-width
    ci_lower = (n - 1) * variance_means / chi2_lower
    ci_upper = (n - 1) * variance_means / chi2_upper
    ci_half_width = (ci_upper - ci_lower) / 2
    print("99% Confidence Interval Half-Width for Variances:")
    print(ci_half_width)
    print("**********************************************************************************")

    # Relative error
    print("Relative Error in Variance Estimates:")
    print(ci_half_width / variance_means)
    print("**********************************************************************************")

    # Required number of epochs for half-width = 5
    required_n_5 = ((n - 1) * variance_means / ((5 + ci_half_width) ** 2)) * scs.chi2.ppf(1 - alpha / 2, df=n - 1)
    print("Number of epochs required for 99% confidence, half-width 5 units for all variance measures:")
    print(np.ceil(required_n_5.max()))
    print("**********************************************************************************")

    # Required number of epochs for half-width = 10
    required_n_10 = ((n - 1) * variance_means / ((10 + ci_half_width) ** 2)) * scs.chi2.ppf(1 - alpha / 2, df=n - 1)
    print("Number of epochs required for 99% confidence, half-width 10 units for all variance measures:")
    print(np.ceil(required_n_10.max()))

# Call the simulation function if this script is run directly
if __name__ == "__main__":
    run_multi_queue_simulation()