from dataclasses import dataclass

@dataclass
class ModelParameters:


    leukemia_doctor_1_mean_service_time_regular: int = 20
    leukemia_doctor_1_mean_service_time_complex: int = 40
    leukemia_doctor_1_number_of_regular_patients: int = 8
    leukemia_doctor_1_number_of_complex_patients: int = 6
    leukemia_doctor_1_probability_of_complex_patient: float = leukemia_doctor_1_number_of_complex_patients/(leukemia_doctor_1_number_of_regular_patients + leukemia_doctor_1_number_of_complex_patients)

    leukemia_doctor_2_mean_service_time_regular: int = 20
    leukemia_doctor_2_mean_service_time_complex: int = 40
    leukemia_doctor_2_number_of_regular_patients: int = 8
    leukemia_doctor_2_number_of_complex_patients: int = 2
    leukemia_doctor_2_probability_of_complex_patient: float = leukemia_doctor_2_number_of_complex_patients/(leukemia_doctor_2_number_of_regular_patients + leukemia_doctor_2_number_of_complex_patients)

    transplant_doctor_1_mean_service_time_regular: int = 20
    transplant_doctor_1_mean_service_time_complex: int = 40
    transplant_doctor_1_number_of_regular_patients: int = 12
    transplant_doctor_1_number_of_complex_patients: int = 1
    transplant_doctor_1_probability_of_complex_patient: float = transplant_doctor_1_number_of_complex_patients/(transplant_doctor_1_number_of_regular_patients + transplant_doctor_1_number_of_complex_patients)

    transplant_doctor_2_mean_service_time_regular: int = 20
    transplant_doctor_2_mean_service_time_complex: int = 40
    transplant_doctor_2_number_of_regular_patients: int = 13
    transplant_doctor_2_number_of_complex_patients: int = 4
    transplant_doctor_2_probability_of_complex_patient: float = transplant_doctor_2_number_of_complex_patients/(transplant_doctor_2_number_of_regular_patients + transplant_doctor_2_number_of_complex_patients)

    transplant_doctor_3_mean_service_time_regular: int = 20
    transplant_doctor_3_mean_service_time_complex: int = 40
    transplant_doctor_3_number_of_regular_patients: int = 16
    transplant_doctor_3_number_of_complex_patients: int = 1
    transplant_doctor_3_probability_of_complex_patient: float = transplant_doctor_3_number_of_complex_patients/(transplant_doctor_3_number_of_regular_patients + transplant_doctor_3_number_of_complex_patients)

    number_of_other_patients: int = 30
    probability_of_complex_other_patient: float = 0.2 #guesstimate

    nurse_mean_service_time_regular: int = 20
    nurse_mean_service_time_complex: int = 40

    probability_of_visiting_nurse_leukemia: float = 10/13 #according to analysis.ipynb proportion_no_scheduled_nurse_visit_time_leukemia: 0.23076923076923078 (3/13)
    probability_of_visiting_nurse_transplant: float = 1 #according to staff testimonies
    probability_of_visiting_nurse_other: float = 4/5 #guesstimate

    nurse_station_1_assignment_probability_leukemia: float = 0.2
    nurse_station_2_assignment_probability_leukemia: float = 0.2
    nurse_station_3_assignment_probability_leukemia: float = 0.2
    nurse_station_4_assignment_probability_leukemia: float = 0.2
    nurse_station_5_assignment_probability_leukemia: float = 0.2
    nurse_station_6_assignment_probability_leukemia: float = 0

    nurse_station_1_assignment_probability_transplant: float = 1/6
    nurse_station_2_assignment_probability_transplant: float = 1/6
    nurse_station_3_assignment_probability_transplant: float = 1/6
    nurse_station_4_assignment_probability_transplant: float = 1/6
    nurse_station_5_assignment_probability_transplant: float = 1/6
    nurse_station_6_assignment_probability_transplant: float = 1/6

    # nurse_station_1_assignment_probability_leukemia: float = 0.3
    # nurse_station_2_assignment_probability_leukemia: float = 0
    # nurse_station_3_assignment_probability_leukemia: float = 0
    # nurse_station_4_assignment_probability_leukemia: float = 0.2
    # nurse_station_5_assignment_probability_leukemia: float = 0.5
    # nurse_station_6_assignment_probability_leukemia: float = 0

    # nurse_station_1_assignment_probability_transplant: float = 1/7
    # nurse_station_2_assignment_probability_transplant: float = 1/7
    # nurse_station_3_assignment_probability_transplant: float = 1/14
    # nurse_station_4_assignment_probability_transplant: float = 2/7
    # nurse_station_5_assignment_probability_transplant: float = 1/7
    # nurse_station_6_assignment_probability_transplant: float = 3/14

    nurse_station_1_assignment_probability_other: float = 1/5
    nurse_station_2_assignment_probability_other: float = 1/5
    nurse_station_3_assignment_probability_other: float = 1/5
    nurse_station_4_assignment_probability_other: float = 1/5
    nurse_station_5_assignment_probability_other: float = 1/5
    nurse_station_6_assignment_probability_other: float = 0

    q_flow_mean_service_time = 1
    secretary_mean_service_time = 4