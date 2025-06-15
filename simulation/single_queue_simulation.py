import os

import pandas as pd
import numpy as np
import scipy.stats as scs
from tqdm import tqdm

from python_sim import SimFunctions, SimClasses
from model_parameters import ModelParametersSingleQueue
from simulation_configuration import SimulationConfiguration
import utils as utils


# Initializing event calendar
Calendar = SimClasses.EventCalendar()

model_parameters = ModelParametersSingleQueue()
simulation_configuration = SimulationConfiguration()

q_flow_station = SimClasses.Resource()
q_flow_station.SetUnits(1)
q_flow_station_queue = SimClasses.FIFOQueue()

secretary_station = SimClasses.Resource()
secretary_station.SetUnits(2)

secretary_station_queue = SimClasses.FIFOQueue()

general_nurse_station = SimClasses.Resource()
general_nurse_station.SetUnits(5)
transplant_nurse_station = SimClasses.Resource()
transplant_nurse_station.SetUnits(1)

general_nurse_station_queue = SimClasses.FIFOQueue()
transplant_nurse_station_queue = SimClasses.FIFOQueue()

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

general_nurse_station_wait_time = SimClasses.DTStat()
transplant_nurse_station_wait_time = SimClasses.DTStat()

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

general_nurse_station_scheduled_vs_actual_time_diff = SimClasses.DTStat()
transplant_nurse_station_scheduled_vs_actual_time_diff = SimClasses.DTStat()

q_flow_station_wait_time_avg = []
q_flow_station_wait_time_var = []

secretary_station_wait_time_avg = []
secretary_station_wait_time_var = []

general_nurse_station_wait_time_avg = []
general_nurse_station_wait_time_var = []
transplant_nurse_station_wait_time_avg = []
transplant_nurse_station_wait_time_var = []

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

general_nurse_station_queue_length_avg = []
general_nurse_station_queue_length_var = []

transplant_nurse_station_queue_length_avg = []
transplant_nurse_station_queue_length_var = []

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

general_nurse_station_busy_avg = []
general_nurse_station_busy_var = []

transplant_nurse_station_busy_avg = []
transplant_nurse_station_busy_var = []


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

general_nurse_station_queue_length = []
transplant_nurse_station_queue_length = []

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

general_nurse_station_scheduled_vs_actual_time_diff_avg = []
transplant_nurse_station_scheduled_vs_actual_time_diff_avg = []

general_nurse_station_scheduled_vs_actual_time_diff_var = []
transplant_nurse_station_scheduled_vs_actual_time_diff_var = []

pbar_outer = tqdm(total=simulation_configuration.num_epochs, desc="Running Simulation")
for epoch in range(simulation_configuration.num_epochs):
    SimFunctions.SimFunctionsInit(Calendar)
    list_of_patients = utils.generate_patients(Calendar, model_parameters)
    for patient_list in list_of_patients:
        for patient in patient_list:
            nurse_station = utils.assign_nurse_station_single_queue(patient.get_type(), patient.complexity_level, model_parameters)
            patient.set_nurse_name(nurse_station)

    nurse_num_patients = {"general_nurse_station": sum([utils.get_nurse_number_of_patients_single_queue(patient_list, "general_nurse_station") for patient_list in list_of_patients]),
                          "transplant_nurse_station": sum([utils.get_nurse_number_of_patients_single_queue(patient_list, "transplant_nurse_station") for patient_list in list_of_patients])}
    counters = {"general_nurse_station": 0, "transplant_nurse_station": 0}

    if epoch == 0:
        print(nurse_num_patients)
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
            
            utils.secretary_station_service_end_multi_queue(NextEvent.WhichObject, model_parameters, secretary_station, secretary_station_queue, secretary_station_wait_time, Calendar)
        
        elif NextEvent.EventType == "general_nurse_station_start_of_waiting":
            general_nurse_station_queue_length.append(general_nurse_station_queue.NumQueue())
            utils.general_nurse_station_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, model_parameters, general_nurse_station_queue, general_nurse_station, general_nurse_station_wait_time, Calendar)
        
        elif NextEvent.EventType == "general_nurse_station_service_start":
            utils.general_nurse_station_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "general_nurse_station_service_end":
            counters["general_nurse_station"] += 1
            if counters["general_nurse_station"] == nurse_num_patients["general_nurse_station"]:
                general_nurse_station_busy_avg.append(general_nurse_station.Mean())
                general_nurse_station_busy_var.append(general_nurse_station.Variance())
            utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
            utils.general_nurse_station_service_end(NextEvent.WhichObject, general_nurse_station, general_nurse_station_queue, general_nurse_station_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_nurse_station_start_of_waiting":
            transplant_nurse_station_queue_length.append(transplant_nurse_station_queue.NumQueue())
            utils.transplant_nurse_station_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_nurse_station_queue, transplant_nurse_station, transplant_nurse_station_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_nurse_station_service_start":
            utils.transplant_nurse_station_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "transplant_nurse_station_service_end":
            counters["transplant_nurse_station"] += 1
            if counters["transplant_nurse_station"] == nurse_num_patients["transplant_nurse_station"]:
                transplant_nurse_station_busy_avg.append(transplant_nurse_station.Mean())  # Use actual busy time
                transplant_nurse_station_busy_var.append(transplant_nurse_station.Variance())  # Use actual busy time variance
            utils.set_patient_blood_test_results_ready_time(NextEvent.WhichObject, Calendar, model_parameters)
            utils.transplant_nurse_station_service_end(NextEvent.WhichObject, transplant_nurse_station, transplant_nurse_station_queue, transplant_nurse_station_wait_time, Calendar)
        
        elif NextEvent.EventType == "receive_blood_test_results":
            NextEvent.WhichObject.receive_blood_test_results()
        
        elif NextEvent.EventType == "leukemia_doctor_1_start_of_waiting":
            leukemia_doctor_1_queue_length.append(leukemia_doctor_1_queue.NumQueue())
            utils.leukemia_doctor_1_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, leukemia_doctor_1_queue, leukemia_doctor_1, leukemia_doctor_1_wait_time, Calendar)   

        elif NextEvent.EventType == "leukemia_doctor_1_service_start":
            utils.leukemia_doctor_1_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "leukemia_doctor_1_service_end":
            utils.leukemia_doctor_1_service_end(NextEvent.WhichObject, leukemia_doctor_1, leukemia_doctor_1_queue, leukemia_doctor_1_wait_time, Calendar)
        
        elif NextEvent.EventType == "leukemia_doctor_2_start_of_waiting":
            leukemia_doctor_2_queue_length.append(leukemia_doctor_2_queue.NumQueue())
            utils.leukemia_doctor_2_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, leukemia_doctor_2_queue, leukemia_doctor_2, leukemia_doctor_2_wait_time, Calendar)
        
        elif NextEvent.EventType == "leukemia_doctor_2_service_start":
            utils.leukemia_doctor_2_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "leukemia_doctor_2_service_end":
            utils.leukemia_doctor_2_service_end(NextEvent.WhichObject, leukemia_doctor_2, leukemia_doctor_2_queue, leukemia_doctor_2_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_1_start_of_waiting":
            transplant_doctor_1_queue_length.append(transplant_doctor_1_queue.NumQueue())
            utils.transplant_doctor_1_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_doctor_1_queue, transplant_doctor_1, transplant_doctor_1_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_1_service_start":
            utils.transplant_doctor_1_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_1_service_end":
            utils.transplant_doctor_1_service_end(NextEvent.WhichObject, transplant_doctor_1, transplant_doctor_1_queue, transplant_doctor_1_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_2_start_of_waiting":
            transplant_doctor_2_queue_length.append(transplant_doctor_2_queue.NumQueue())
            utils.transplant_doctor_2_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_doctor_2_queue, transplant_doctor_2, transplant_doctor_2_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_2_service_start":
            utils.transplant_doctor_2_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_2_service_end":
            utils.transplant_doctor_2_service_end(NextEvent.WhichObject, transplant_doctor_2, transplant_doctor_2_queue, transplant_doctor_2_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_3_start_of_waiting":
            transplant_doctor_3_queue_length.append(transplant_doctor_3_queue.NumQueue())
            utils.transplant_doctor_3_start_of_waiting(NextEvent.WhichObject, SimClasses.Clock, transplant_doctor_3_queue, transplant_doctor_3, transplant_doctor_3_wait_time, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_3_service_start":
            utils.transplant_doctor_3_service_start(NextEvent.WhichObject, model_parameters, Calendar)
        
        elif NextEvent.EventType == "transplant_doctor_3_service_end":
            utils.transplant_doctor_3_service_end(NextEvent.WhichObject, transplant_doctor_3, transplant_doctor_3_queue, transplant_doctor_3_wait_time, Calendar)
        
        elif NextEvent.EventType == "process_complete" or NextEvent.EventType == "other_start_of_waiting":
            #here the process ends for the other patients
            utils.process_complete_single_queue(NextEvent.WhichObject, SimClasses.Clock,
                                   general_nurse_station_scheduled_vs_actual_time_diff, transplant_nurse_station_scheduled_vs_actual_time_diff,
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
    general_nurse_station_wait_time_avg.append(general_nurse_station_wait_time.Mean())
    general_nurse_station_wait_time_var.append(general_nurse_station_wait_time.StdDev()**2)
    transplant_nurse_station_wait_time_avg.append(transplant_nurse_station_wait_time.Mean())
    transplant_nurse_station_wait_time_var.append(transplant_nurse_station_wait_time.StdDev()**2)
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
    general_nurse_station_queue_length_avg.append(general_nurse_station_queue.Mean())
    general_nurse_station_queue_length_var.append(general_nurse_station_queue.Variance())
    transplant_nurse_station_queue_length_avg.append(transplant_nurse_station_queue.Mean())
    transplant_nurse_station_queue_length_var.append(transplant_nurse_station_queue.Variance())
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

    general_nurse_station_scheduled_vs_actual_time_diff_avg.append(general_nurse_station_scheduled_vs_actual_time_diff.Mean())
    transplant_nurse_station_scheduled_vs_actual_time_diff_avg.append(transplant_nurse_station_scheduled_vs_actual_time_diff.Mean())

    general_nurse_station_scheduled_vs_actual_time_diff_var.append(general_nurse_station_scheduled_vs_actual_time_diff.StdDev()**2)
    transplant_nurse_station_scheduled_vs_actual_time_diff_var.append(transplant_nurse_station_scheduled_vs_actual_time_diff.StdDev()**2)

    if epoch == 0:
        utils.generate_patient_attributes_csv(list_of_patients, "results_directory/single_queue/patient_attributes.csv")

    pbar_outer.set_description(f"Running Simulation - {epoch+1}/{simulation_configuration.num_epochs}")

    pbar_outer.update(1)

pbar_outer.close()
print("Simulation completed")

averages_df = pd.DataFrame({
    "q_flow_station_wait_time_avg": q_flow_station_wait_time_avg,
    "q_flow_station_queue_length_avg": q_flow_station_queue_length_avg,
    "q_flow_station_busy_avg": q_flow_station_busy_avg,
    "secretary_station_wait_time_avg": secretary_station_wait_time_avg,
    "secretary_station_queue_length_avg": secretary_station_queue_length_avg,
    "secretary_station_busy_avg": secretary_station_busy_avg,
    "general_nurse_station_wait_time_avg": general_nurse_station_wait_time_avg,
    "general_nurse_station_queue_length_avg": general_nurse_station_queue_length_avg,
    "general_nurse_station_busy_avg": general_nurse_station_busy_avg,
    "transplant_nurse_station_wait_time_avg": transplant_nurse_station_wait_time_avg,
    "transplant_nurse_station_queue_length_avg": transplant_nurse_station_queue_length_avg,
    "transplant_nurse_station_busy_avg": transplant_nurse_station_busy_avg,
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
    "general_nurse_station_scheduled_vs_actual_time_diff_avg": general_nurse_station_scheduled_vs_actual_time_diff_avg,
    "transplant_nurse_station_scheduled_vs_actual_time_diff_avg": transplant_nurse_station_scheduled_vs_actual_time_diff_avg
    })

os.makedirs("results_directory/single_queue", exist_ok=True)
averages_df.to_csv(f"results_directory/single_queue/averages_data.csv")
print(f"Simulation Results Saved to results_directory/single_queue/averages_data.csv")
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
    "general_nurse_station_wait_time_var": general_nurse_station_wait_time_var,
    "general_nurse_station_queue_length_var": general_nurse_station_queue_length_var,
    "general_nurse_station_busy_var": general_nurse_station_busy_var,
    "transplant_nurse_station_wait_time_var": transplant_nurse_station_wait_time_var,
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
    "general_nurse_station_scheduled_vs_actual_time_diff_var": general_nurse_station_scheduled_vs_actual_time_diff_var,
    "transplant_nurse_station_scheduled_vs_actual_time_diff_var": transplant_nurse_station_scheduled_vs_actual_time_diff_var
})

os.makedirs("results_directory/single_queue", exist_ok=True)
variances_df.to_csv(f"results_directory/single_queue/variances_data.csv")
print("Simulation Variance Results Saved to results_directory/single_queue/variances_data.csv")
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