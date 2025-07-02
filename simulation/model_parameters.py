from dataclasses import dataclass


@dataclass
class ModelParametersMultiQueue:

    scaler = 0.85

    leukemia_doctor_1_mean_service_time_regular: int = 15
    leukemia_doctor_1_mean_service_time_complex: int = 20
    leukemia_doctor_1_number_of_regular_patients: int = int(8 * scaler)
    leukemia_doctor_1_number_of_complex_patients: int = int(6 * scaler)
    leukemia_doctor_1_number_of_patients = leukemia_doctor_1_number_of_regular_patients + leukemia_doctor_1_number_of_complex_patients
    leukemia_doctor_1_probability_of_complex_patient: float = leukemia_doctor_1_number_of_complex_patients/(leukemia_doctor_1_number_of_regular_patients + leukemia_doctor_1_number_of_complex_patients)

    leukemia_doctor_2_mean_service_time_regular: int = 15
    leukemia_doctor_2_mean_service_time_complex: int = 20
    leukemia_doctor_2_number_of_regular_patients: int = int(8 * scaler)
    leukemia_doctor_2_number_of_complex_patients: int = 2
    leukemia_doctor_2_number_of_patients = leukemia_doctor_2_number_of_regular_patients + leukemia_doctor_2_number_of_complex_patients
    leukemia_doctor_2_probability_of_complex_patient: float = leukemia_doctor_2_number_of_complex_patients/(leukemia_doctor_2_number_of_regular_patients + leukemia_doctor_2_number_of_complex_patients)

    transplant_doctor_1_mean_service_time_regular: int = 15
    transplant_doctor_1_mean_service_time_complex: int = 20
    transplant_doctor_1_number_of_regular_patients: int = int(12 * scaler)
    transplant_doctor_1_number_of_complex_patients: int = 1
    transplant_doctor_1_number_of_patients = transplant_doctor_1_number_of_regular_patients + transplant_doctor_1_number_of_complex_patients
    transplant_doctor_1_probability_of_complex_patient: float = transplant_doctor_1_number_of_complex_patients/(transplant_doctor_1_number_of_regular_patients + transplant_doctor_1_number_of_complex_patients)

    transplant_doctor_2_mean_service_time_regular: int = 15
    transplant_doctor_2_mean_service_time_complex: int = 20
    transplant_doctor_2_number_of_regular_patients: int = int(13 * scaler)
    transplant_doctor_2_number_of_complex_patients: int = int(4 * scaler)
    transplant_doctor_2_number_of_patients = transplant_doctor_2_number_of_regular_patients + transplant_doctor_2_number_of_complex_patients
    transplant_doctor_2_probability_of_complex_patient: float = transplant_doctor_2_number_of_complex_patients/(transplant_doctor_2_number_of_regular_patients + transplant_doctor_2_number_of_complex_patients)

    transplant_doctor_3_mean_service_time_regular: int = 15
    transplant_doctor_3_mean_service_time_complex: int = 20
    transplant_doctor_3_number_of_regular_patients: int = int(16 * scaler)
    transplant_doctor_3_number_of_complex_patients: int = 1
    transplant_doctor_3_number_of_patients = transplant_doctor_3_number_of_regular_patients + transplant_doctor_3_number_of_complex_patients
    transplant_doctor_3_probability_of_complex_patient: float = transplant_doctor_3_number_of_complex_patients/(transplant_doctor_3_number_of_regular_patients + transplant_doctor_3_number_of_complex_patients)

    number_of_other_patients: int = 20
    probability_of_complex_other_patient: float = 0.2 #guesstimate

    nurse_mean_service_time_regular: int = 15
    nurse_mean_service_time_complex: int = 20

    transplant_nurse_mean_service_time: int = 30 #this is nurse 6

    probability_of_visiting_nurse_leukemia: float = 10/13 #according to analysis.ipynb proportion_no_scheduled_nurse_visit_time_leukemia: 0.23076923076923078 (3/13)
    probability_of_visiting_nurse_transplant: float = 1 #according to staff testimonies
    probability_of_visiting_nurse_other: float = 4/5 #guesstimate

    #The parameter below is related to one of our suggestions, having some of the regular transplant patients arrive with a blood test
    #thus avoiding the need for a nurse consultation.
    #its here only for reference, as we hardcoded it in the transplant_patient.py file
    #############################################################
    probability_of_visiting_nurse_transplant_regular: float = 4/5
    #############################################################

    nurse_station_1_assignment_probability_leukemia: float = 0.2
    nurse_station_2_assignment_probability_leukemia: float = 0.2
    nurse_station_3_assignment_probability_leukemia: float = 0.2
    nurse_station_4_assignment_probability_leukemia: float = 0.2
    nurse_station_5_assignment_probability_leukemia: float = 0.2
    nurse_station_6_assignment_probability_leukemia: float = 0

    nurse_station_1_assignment_probability_transplant_regular: float = 2/11
    nurse_station_2_assignment_probability_transplant_regular: float = 2/11
    nurse_station_3_assignment_probability_transplant_regular: float = 2/11
    nurse_station_4_assignment_probability_transplant_regular: float = 2/11
    nurse_station_5_assignment_probability_transplant_regular: float = 2/11
    nurse_station_6_assignment_probability_transplant_regular: float = 1/11

    nurse_station_1_assignment_probability_other: float = 1/5
    nurse_station_2_assignment_probability_other: float = 1/5
    nurse_station_3_assignment_probability_other: float = 1/5
    nurse_station_4_assignment_probability_other: float = 1/5
    nurse_station_5_assignment_probability_other: float = 1/5
    nurse_station_6_assignment_probability_other: float = 0

    q_flow_mean_service_time = 1
    secretary_mean_service_time = 4

    probability_of_needing_long_blood_test: float = 0.25 #long = chemistry, o.w. only blood count

    mean_time_for_regular_blood_test: int = 40
    mean_time_for_long_blood_test: int = 120 

    @classmethod
    def from_dict(cls, dict_of_parameters):
        return cls(**dict_of_parameters)

@dataclass
class ModelParametersSingleQueue:

    scaler = 0.85

    leukemia_doctor_1_mean_service_time_regular: int = 15
    leukemia_doctor_1_mean_service_time_complex: int = 20
    leukemia_doctor_1_number_of_regular_patients: int = int(8 * scaler)
    leukemia_doctor_1_number_of_complex_patients: int = int(6 * scaler)
    leukemia_doctor_1_number_of_patients = leukemia_doctor_1_number_of_regular_patients + leukemia_doctor_1_number_of_complex_patients
    leukemia_doctor_1_probability_of_complex_patient: float = leukemia_doctor_1_number_of_complex_patients/(leukemia_doctor_1_number_of_regular_patients + leukemia_doctor_1_number_of_complex_patients)

    leukemia_doctor_2_mean_service_time_regular: int = 15
    leukemia_doctor_2_mean_service_time_complex: int = 20
    leukemia_doctor_2_number_of_regular_patients: int = int(8 * scaler)
    leukemia_doctor_2_number_of_complex_patients: int = 2
    leukemia_doctor_2_number_of_patients = leukemia_doctor_2_number_of_regular_patients + leukemia_doctor_2_number_of_complex_patients
    leukemia_doctor_2_probability_of_complex_patient: float = leukemia_doctor_2_number_of_complex_patients/(leukemia_doctor_2_number_of_regular_patients + leukemia_doctor_2_number_of_complex_patients)

    transplant_doctor_1_mean_service_time_regular: int = 15
    transplant_doctor_1_mean_service_time_complex: int = 20
    transplant_doctor_1_number_of_regular_patients: int = int(12 * scaler)
    transplant_doctor_1_number_of_complex_patients: int = 1
    transplant_doctor_1_number_of_patients = transplant_doctor_1_number_of_regular_patients + transplant_doctor_1_number_of_complex_patients
    transplant_doctor_1_probability_of_complex_patient: float = transplant_doctor_1_number_of_complex_patients/(transplant_doctor_1_number_of_regular_patients + transplant_doctor_1_number_of_complex_patients)

    transplant_doctor_2_mean_service_time_regular: int = 15
    transplant_doctor_2_mean_service_time_complex: int = 20
    transplant_doctor_2_number_of_regular_patients: int = int(13 * scaler)
    transplant_doctor_2_number_of_complex_patients: int = int(4 * scaler)
    transplant_doctor_2_number_of_patients = transplant_doctor_2_number_of_regular_patients + transplant_doctor_2_number_of_complex_patients
    transplant_doctor_2_probability_of_complex_patient: float = transplant_doctor_2_number_of_complex_patients/(transplant_doctor_2_number_of_regular_patients + transplant_doctor_2_number_of_complex_patients)

    transplant_doctor_3_mean_service_time_regular: int = 15
    transplant_doctor_3_mean_service_time_complex: int = 20
    transplant_doctor_3_number_of_regular_patients: int = int(16 * scaler)
    transplant_doctor_3_number_of_complex_patients: int = 1
    transplant_doctor_3_number_of_patients = transplant_doctor_3_number_of_regular_patients + transplant_doctor_3_number_of_complex_patients
    transplant_doctor_3_probability_of_complex_patient: float = transplant_doctor_3_number_of_complex_patients/(transplant_doctor_3_number_of_regular_patients + transplant_doctor_3_number_of_complex_patients)

    number_of_other_patients: int = 20
    probability_of_complex_other_patient: float = 0.2 #guesstimate

    nurse_mean_service_time_regular: int = 15
    nurse_mean_service_time_complex: int = 20

    transplant_nurse_mean_service_time: int = 30

    probability_of_visiting_nurse_leukemia: float = 10/13 #according to analysis.ipynb proportion_no_scheduled_nurse_visit_time_leukemia: 0.23076923076923078 (3/13)
    probability_of_visiting_nurse_transplant: float = 1 #according to staff testimonies
    probability_of_visiting_nurse_other: float = 4/5 #guesstimate
    

    general_nurse_station_assignment_probability_transplant_regular: float = 10/11
    transplant_nurse_station_assignment_probability_transplant_regular: float = 1/11

    general_nurse_station_preparation_time_buffer: int = 3 #minutes for preparation

    q_flow_mean_service_time = 1
    secretary_mean_service_time = 4

    probability_of_needing_long_blood_test: float = 0.25 #long = chemistry, o.w. only blood count

    #The parameter below is related to one of our suggestions, having some of the regular transplant patients arrive with a blood test
    #thus avoiding the need for a nurse consultation.
    #its here only for reference, as we hardcoded it in the transplant_patient.py file
    #############################################################
    probability_of_visiting_nurse_transplant_regular: float = 4/5
    #############################################################

    mean_time_for_regular_blood_test: int = 40
    mean_time_for_long_blood_test: int = 120 

    @classmethod
    def from_dict(cls, dict_of_parameters):
        return cls(**dict_of_parameters)