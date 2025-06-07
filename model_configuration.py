from typing import Dict, Any

class ModelConfig:
    def __init__(self, queueing_policy: str):
        """
        Initialize the ModelConfig with a specific queueing policy.

        Args:
            queueing_policy (str): The type of queueing policy to use ('single' or 'per-server')
        """
        self._simulation_parameters = self._initialize_simulation_parameters(queueing_policy)

    def _initialize_simulation_parameters(self, queueing_policy: str) -> dict:
        """
        Initialize all simulation parameters.

        Args:
            queueing_policy (str): The type of queueing policy to use

        Returns:
            dict: Dictionary containing all simulation parameters
        """
        return {
            "queue_policy": self._initialize_queue_policy(queueing_policy),
            "arrival": self._initialize_arrival_params(),
            "q_flow": self._initialize_q_flow_params(),
            "secretary": self._initialize_secretary_params(),
            "nurses": self._initialize_nurse_params(),
            "lab": self._initialize_lab_params(),
            "doctors": self._initialize_doctor_params(),
            "patients": self._initialize_patient_params(),
        }

    def _initialize_queue_policy(self, queueing_policy: str) -> str:
        """
        Initialize the queue policy.

        Args:
            queueing_policy (str): The type of queueing policy to use

        Returns:
            str: The queueing policy type
        """
        return queueing_policy

    def _initialize_q_flow_params(self) -> dict:
        return {
            "mean_service_time": 0.5,  # in minutes
            "distribution": "exponential",
        }

    def _initialize_secretary_params(self) -> dict:
        return {
            "mean_service_time": 0.75,
            "distribution": "exponential",
        }

    def _initialize_nurses_params(self) -> dict:
        return {
            "num_servers": 5,
            "mean_service_time_regular": 20.0,
            "mean_service_time_complex": 40.0,
            "distribution": "exponential",
        }

    def _initialize_lab_params(self) -> dict:
        return {
            "return_time_regular_test": 120.0,
            "return_time_complex_test": 300.0,
            "distribution": "exponential",
        }

    def _initialize_doctor_params(self) -> Dict[str, dict]:
        return {
            "Leukemia1": {
                "mean_service_time_other": 20.0, #Non Leukemia
                "mean_service_time_regular": 15.0, #Leukemia low complexity
                "mean_service_time_complex": 25.0, #Leukemia high complexity
                "distribution": "exponential",
                "capacity": 15,
            },
            "Leukemia2": {
                "mean_service_time_other": 20.0, #Non Leukemia
                "mean_service_time_regular": 15.0, #Leukemia low complexity
                "mean_service_time_complex": 25.0, #Leukemia high complexity
                "distribution": "exponential",
                "capacity": 15,
            },
            "Transplant": {
                "mean_service_time_other": 20.0, #Non Transplant
                "mean_service_time_regular": 15.0, #Transplant low complexity
                "mean_service_time_complex": 25.0, #Transplant high complexity
                "distribution": "exponential",
                "capacity": 20,
            },
        }

    def _initialize_patients_params(self) -> Dict[str, Any]:
        return {
            "probability_of_leukemia": 0.35,
            "probability_of_transplant": 0.15,
            # probability of "Other" is 1 - (probability of leukemia + probability of transplant)
            "Transplant" : {
                "number_of_patients": 20,
                "probability_of_needing_a_test": 0.25, #25% of the time, the patient needs a test to be done by the nurse
                "probability_of_regular_test": 0.75, #75% of the time a test is needed, it is a regular test
                # probability of complex test is 1 - probability of regular test
                "doctor_needs_tests": 0.2, #20% of the time the doctor must get the results from the lab before seeing the patient
            },
            "Leukemia" : {
                "number_of_patients": 30,
                "probability_of_needing_a_test": 1,
                "probability_of_regular_test": 0.75, #75% of the time it is a regular test
                # probability of complex test is 1 - probability of regular test
                "doctor_needs_tests": 0.2, #20% of the time the doctor must get the results from the lab before seeing the patient
            },
            "Other": {
                "number_of_patients": 100,
                "probability_of_needing_a_test": 0.5,
                "probability_of_regular_test": 0.75,
                # probability of complex test is 1 - probability of regular test
                "doctor_needs_tests": 0.2,
            },
        }

    @property
    def simulation_parameters(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all simulation parameters and configurations.

        The dictionary includes the following key components:
        - queue_policy: Queue management policy settings
        - arrival: Patient arrival rate parameters
        - q_flow: Queue flow service parameters
        - secretary: Secretary service parameters
        - nurses: Nurse service parameters including regular and complex test times
        - lab: Laboratory test parameters for regular and complex tests
        - doctors: Doctor service parameters for different specialties (Leukemia1, Leukemia2, Transplant)
        - patients: Patient type probabilities and test requirements for different conditions

        Returns:
            dict: A dictionary containing all simulation configuration parameters
        """
        return self._simulation_parameters
    
    @property
    def patient_params(self) -> Dict[str, Any]:
        return self._simulation_parameters["patients"]
    
    @property
    def doctor_params(self) -> Dict[str, Any]:
        return self._simulation_parameters["doctors"]
    
    @property
    def lab_params(self) -> Dict[str, Any]:
        return self._simulation_parameters["lab"]
    
    @property
    def nurse_params(self) -> Dict[str, Any]:
        return self._simulation_parameters["nurses"]
    
    @property
    def q_flow_params(self) -> Dict[str, Any]:
        return self._simulation_parameters["q_flow"]
    
    @property
    def secretary_params(self) -> Dict[str, Any]:
        return self._simulation_parameters["secretary"]
