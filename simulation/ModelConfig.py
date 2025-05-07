import math

class ModelConfig:
    def __init__(self):
        self.params = self._initialize_params()

    def _initialize_params(self):
        return {
            "queue_policy": self._initialize_queue_policy(),
            "arrival": self._initialize_arrival_params(),
            "q_flow": self._initialize_q_flow_params(),
            "secretary": self._initialize_secretary_params(),
            "nurses": self._initialize_nurse_params(),
            "lab": self._initialize_lab_params(),
            "doctors": self._initialize_doctor_params(),
            "patients": self._initialize_patient_params(),
        }

    def _initialize_queue_policy(self):
        return {
            "type": "single",  # or "per-server"
        }

    def _initialize_arrival_params(self):
        return {
            "time_varying_rate": lambda t: 6 + 4 * math.sin(t / 60)  # example, for constant rate, use lambda t: rate
        }

    def _initialize_q_flow_params(self):
        return {
            "mean_service_time": 0.5,  # in minutes
            "distribution": "exponential",
        }

    def _initialize_secretary_params(self):
        return {
            "mean_service_time": 0.75,
            "distribution": "exponential",
        }

    def _initialize_nurses_params(self):
        return {
            "num_servers": 5,
            "mean_service_time_regular": 20.0,
            "mean_service_time_complex": 40.0,
            "distribution": "exponential",
        }

    def _initialize_lab_params(self):
        return {
            "return_time_regular_test": 120.0,
            "return_time_complex_test": 240.0,
            "distribution": "exponential",
        }

    def _initialize_doctor_params(self):
        return {
            "Leukemia1": {
                "mean_service_time_other": 20.0, #Non Leukemia
                "mean_service_time_regular": 15.0, #Leukemia low complexity
                "mean_service_time_complex": 25.0, #Leukemia high complexity
                "distribution": "exponential",
                "daily_capacity": 15, #Assigned up to 15 patients per day
            },
            "Leukemia2": {
                "mean_service_time_other": 20.0, #Non Leukemia
                "mean_service_time_regular": 15.0, #Leukemia low complexity
                "mean_service_time_complex": 25.0, #Leukemia high complexity
                "distribution": "exponential",
                "daily_capacity": 15, #Assigned up to 15 patients per day
            },
            "Myeloma": {
                "mean_service_time_other": 20.0, #Non Myeloma
                "mean_service_time_regular": 15.0, #Myeloma low complexity
                "mean_service_time_complex": 25.0, #Myeloma high complexity
                "distribution": "exponential",
                "daily_capacity": 20, #Assigned up to 20 patients per day
            },
        }

    def _initialize_patients_params(self):
        return {
            "probability_of_leukemia": 0.35,
            "probability_of_myeloma": 0.15,
            "probability_of_other": 0.5,
            "Myeloma" : {
                "probability_of_needing_a_test": 0.25, #25% of the time, the patient needs a test to be done by the nurse
                "probability_of_regular_test": 0.75, #75% of the time a test is needed, it is a regular test
                "probability_of_complex_test": 0.25, #25% of the time a test is needed, it is a complex test
                "probability_that_doctor_must_get_results_from_lab": 0.2, #20% of the time the doctor must get the results from the lab before seeing the patient
            },
            "Leukemia" : {
                "probability_of_regular_test": 0.75, #75% of the time it is a regular test
                "probability_of_complex_test": 0.25, #25% of the time it is a complex test
                "probability_that_doctor_must_get_results_from_lab": 0.2, #20% of the time the doctor must get the results from the lab before seeing the patient
            },
        }

    def get(self, section):
        return self.params.get(section)
