from python_sim import SimClasses
from patient import Patient, PatientType, TestType
from numpy.random import exponential
from python_sim.SimFunctions import SchedulePlus

class Doctor(SimClasses.Resource):
    def __init__(self, name: str, config: dict, doctor_config: dict):
        """
        Doctor constructor.

        Args:
            name (str): Doctor name, must match a key in the doctor_config dictionary (e.g., 'Leukemia1', 'Transplant')
            config (dict): The full simulation config (from ModelConfig.simulation_parameters)
            doctor_config (dict): Specific config for this doctor from config['doctors'][name]
        """
        super().__init__()
        self.name = name
        self.config = config
        self.doctor_config = doctor_config
        self.daily_capacity = doctor_config["daily_capacity"]
        self.current_patient = None
        self.busy = False

    def try_start_service(self, patient: Patient, calendar):
        """Begins service for a patient if doctor is free."""
        if self.CurrentNumBusy >= self.NumberOfUnits:
            return  # Doctor is busy

        self.current_patient = patient
        self.Seize(1)
        self.busy = True
        patient.doctor_service_start_time = SimClasses.Clock
        service_time = self.get_service_time(patient)
        SchedulePlus(calendar, "EndDoctorService", service_time, self)

    def end_service(self):
        """Ends the service for the current patient."""
        self.Free(1)
        self.busy = False
        if self.current_patient:
            self.current_patient.doctor_service_end_time = SimClasses.Clock
            self.current_patient = None

    def get_service_time(self, patient: Patient) -> float:
        """
        Determines doctor's service time for a patient based on condition and test type.

        Returns:
            float: Sampled exponential service time.
        """
        distribution = self.doctor_config.get("distribution", "exponential")
        if distribution != "exponential":
            raise NotImplementedError("Only exponential distribution is currently supported.")

        # If doctor does NOT require test results, use 'other' time
        if patient.patient_type == PatientType.OTHER:
            return exponential(scale=self.doctor_config["mean_service_time_other"])

        if not patient.needs_test or not patient.doctor_needs_test_results:
            return exponential(scale=self.doctor_config["mean_service_time_other"])

        # Handle leukemia/transplant with test results needed
        if patient.test_type == TestType.REGULAR:
            return exponential(scale=self.doctor_config["mean_service_time_regular"])
        elif patient.test_type == TestType.COMPLEX:
            return exponential(scale=self.doctor_config["mean_service_time_complex"])
        else:
            raise ValueError(f"Invalid test type {patient.test_type}")
