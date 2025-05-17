from python_sim import SimClasses, SimFunctions
from queues.queueing_policy import QueueingPolicy
from patient import Patient, TestType
from numpy.random import exponential

class Nurse(SimClasses.Resource):
    def __init__(self, name: str, policy: QueueingPolicy, model_config, buffer_time: float = 0.0):
        """
        Nurse constructor.

        Args:
            name (str): Name of the nurse
            policy (QueueingPolicy): Queue policy managing this nurse
            model_config (ModelConfig): Global simulation configuration object
            buffer_time (float): Optional buffer time before service starts
        """
        super().__init__()
        self.name = name
        self.policy = policy
        self.buffer_time = buffer_time
        self.config = model_config.simulation_parameters["nurses"]
        self.current_patient = None
        self.busy = False

    def try_start_service(self, calendar):
        """Start service for the next patient if available."""
        patient = self.policy.get_next_patient(self.name)
        if patient:
            self.current_patient = patient
            self.Seize(1)
            self.busy = True
            self.policy.record_service_start(self.name, patient)
            if self.buffer_time > 0:
                SimFunctions.SchedulePlus(calendar, "StartNurseService", self.buffer_time, self)
            else:
                self.start_service_immediately(calendar)

    def start_service_immediately(self, calendar):
        """Schedule end of service based on test type."""
        service_duration = self.get_service_time(self.current_patient)
        SimFunctions.SchedulePlus(calendar, "EndNurseService", service_duration, self)

    def end_service(self):
        """End service for the current patient."""
        self.Free(1)
        self.busy = False
        self.current_patient.nurse_service_end_time = SimClasses.Clock
        self.current_patient = None

    def get_service_time(self, patient: Patient) -> float:
        """
        Returns service time for the patient using exponential distribution.

        - Regular test → `mean_service_time_regular`
        - Complex test → `mean_service_time_complex`

        If no test is needed, fallback to `mean_service_time_regular`.

        Args:
            patient (Patient): The patient being served

        Returns:
            float: Sampled service duration
        """
        if not patient.needs_test:
            return exponential(scale=self.config["mean_service_time_regular"])

        if patient.test_type == TestType.REGULAR:
            return exponential(scale=self.config["mean_service_time_regular"])
        elif patient.test_type == TestType.COMPLEX:
            return exponential(scale=self.config["mean_service_time_complex"])
        else:
            raise ValueError(f"Unknown test type: {patient.test_type}")
