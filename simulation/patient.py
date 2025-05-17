from pythonSim.SimClasses import Entity, Clock
from numpy import random
from enum import Enum
from typing import Dict, Any
from utils import truncated_normal_distribution

class PatientType(Enum):
    LEUKEMIA = "leukemia"
    TRANSPLANT = "transplant"
    OTHER = "other"

class TestType(Enum):
    REGULAR = "regular"
    COMPLEX = "complex"

class Patient(Entity):
    def __init__(self, id: int, schedule: dict[str, float], patient_config: Dict[str, Any]):
        # Call parent constructor first to set CreateTime
        super().__init__()
        
        # Store the ID as a separate attribute since Entity doesn't have one
        self.id = id

        self.scheduled_arrival_time = schedule['scheduled_arrival_time']
        self.scheduled_doctor_consultation_time = schedule['scheduled_doctor_consultation_time']

        # Get patient type from config
        self.patient_type = PatientType(patient_config['type'])

        self.assigned_nurse_name = None

        self.assigned_doctor_name = None
        
        # Get probabilities from patient config
        self.needs_test = self.calculate_needs_test(patient_config['probability_of_needing_a_test'])
        self.test_type = self.calculate_test_type(patient_config['probability_of_regular_test']) if self.needs_test else None
        self.doctor_needs_test_results = random.uniform(0, 1) < patient_config['doctor_needs_tests']
        
        self.has_departed = False
        self.total_sojourn_time = 0
        
        # Arrival and departure times
        self.arrival_time = None
        self.departure_time = None

        # Q-Flow timing
        self.q_flow_queue_entry_time = None
        self.q_flow_queue_exit_time = None
        self.q_flow_service_start_time = None
        self.q_flow_service_end_time = None

        # Secretary timing
        self.secretary_queue_entry_time = None
        self.secretary_queue_exit_time = None
        self.secretary_service_start_time = None
        self.secretary_service_end_time = None

        # Nurse timing
        self.nurse_queue_entry_time = None
        self.nurse_queue_exit_time = None
        self.nurse_service_start_time = None
        self.nurse_service_end_time = None

        # Lab test timing
        self.lab_test_queue_entry_time = None
        self.lab_test_queue_exit_time = None
        self.lab_test_service_start_time = None
        self.lab_test_service_end_time = None

        # Doctor timing
        self.doctor_queue_entry_time = None
        self.doctor_queue_exit_time = None
        self.doctor_service_start_time = None
        self.doctor_service_end_time = None

    def calculate_needs_test(self, probability: float) -> bool:
        """Determine if the patient needs a test based on probability."""
        return random.uniform(0, 1) < probability

    def calculate_test_type(self, prob_regular: float) -> TestType:
        """Determine the type of test needed based on probabilities."""
        u = random.uniform(0, 1)
        if u < prob_regular:
            return TestType.REGULAR
        else:
            return TestType.COMPLEX

    def arrive(self) -> None:
        """Arrive at the hospital. Arrival time is a random variable with a normal distribution"""
        self.arrival_time = truncated_normal_distribution(self.scheduled_arrival_time)
        self.q_flow_queue_entry_time = self.arrival_time

    def depart(self) -> None:
        """Depart from the hospital."""
        self.has_departed = True
        self.departure_time = max(
            self.q_flow_service_end_time or 0,
            self.secretary_service_end_time or 0,
            self.nurse_service_end_time or 0,
            self.lab_test_service_end_time or 0,
            self.doctor_service_end_time or 0
        )
        self.total_sojourn_time = self.departure_time - self.arrival_time

    def q_flow_waiting_time(self) -> float:
        """Calculate the waiting time in the queue flow queue."""
        return self.q_flow_queue_exit_time - self.q_flow_queue_entry_time if self.q_flow_queue_exit_time else 0

    def q_flow_service_time(self) -> float:
        """Calculate the service time in the queue flow."""
        return self.q_flow_service_end_time - self.q_flow_service_start_time if self.q_flow_service_end_time else 0

    def q_flow_sojourn_time(self) -> float:
        """Calculate the total time spent in the queue flow system."""
        return self.q_flow_waiting_time() + self.q_flow_service_time()

    def secretary_waiting_time(self) -> float:
        """Calculate the waiting time in the secretary queue."""
        return self.secretary_queue_exit_time - self.secretary_queue_entry_time if self.secretary_queue_exit_time else 0

    def secretary_service_time(self) -> float:
        """Calculate the service time with the secretary."""
        return self.secretary_service_end_time - self.secretary_service_start_time if self.secretary_service_end_time else 0

    def secretary_sojourn_time(self) -> float:
        """Calculate the total time spent in the secretary system."""
        return self.secretary_waiting_time() + self.secretary_service_time()

    def nurse_waiting_time(self) -> float:
        """Calculate the waiting time in the nurse queue."""
        return self.nurse_queue_exit_time - self.nurse_queue_entry_time if self.nurse_queue_exit_time else 0

    def nurse_service_time(self) -> float:
        """Calculate the service time with the nurse."""
        return self.nurse_service_end_time - self.nurse_service_start_time if self.nurse_service_end_time else 0

    def nurse_sojourn_time(self) -> float:
        """Calculate the total time spent in the nurse system."""
        return self.nurse_waiting_time() + self.nurse_service_time()

    def lab_test_waiting_time(self) -> float:
        """Calculate the waiting time in the lab test queue."""
        return self.lab_test_queue_exit_time - self.lab_test_queue_entry_time if self.lab_test_queue_exit_time else 0

    def lab_test_service_time(self) -> float:
        """Calculate the service time in the lab test."""
        return self.lab_test_service_end_time - self.lab_test_service_start_time if self.lab_test_service_end_time else 0

    def lab_test_sojourn_time(self) -> float:
        """Calculate the total time spent in the lab test system."""
        return self.lab_test_waiting_time() + self.lab_test_service_time()

    def doctor_waiting_time(self) -> float:
        """Calculate the waiting time in the doctor queue."""
        return self.doctor_queue_exit_time - self.doctor_queue_entry_time if self.doctor_queue_exit_time else 0

    def doctor_service_time(self) -> float:
        """Calculate the service time with the doctor."""
        return self.doctor_service_end_time - self.doctor_service_start_time if self.doctor_service_end_time else 0

    def doctor_sojourn_time(self) -> float:
        """Calculate the total time spent in the doctor system."""
        return self.doctor_waiting_time() + self.doctor_service_time()

    def total_waiting_time(self) -> float:
        """Calculate the total waiting time across all stations."""
        return (self.q_flow_waiting_time() + 
                self.secretary_waiting_time() + 
                self.nurse_waiting_time() + 
                self.lab_test_waiting_time() + 
                self.doctor_waiting_time())

    def total_service_time(self) -> float:
        """Calculate the total service time across all stations."""
        return (self.q_flow_service_time() + 
                self.secretary_service_time() + 
                self.nurse_service_time() + 
                self.lab_test_service_time() + 
                self.doctor_service_time())

    def assign_nurse(self, nurse_name: str):
        self.assigned_nurse_name = nurse_name
        
    def assign_doctor(self, doctor_name: str):
        self.assigned_doctor_name = doctor_name

    def __str__(self) -> str:
        """String representation of the patient."""
        return (f"Patient {self.id} ({self.patient_type.value}) - "
                f"Test: {self.test_type.value if self.needs_test else 'Not needed'} - "
                f"Status: {'Complete' if self.has_departed else 'In Progress'}")