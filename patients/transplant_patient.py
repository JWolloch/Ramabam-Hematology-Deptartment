from patients.patient import Patient
from datetime import datetime
from python_sim import SimClasses

class TransplantPatient(Patient):
    def __init__(self, schedule: dict[str, datetime], doctor_name: str,
                 probability_of_complex_patient: float,
                 probability_of_visiting_nurse: float):
        super().__init__(schedule, doctor_name, probability_of_complex_patient, probability_of_visiting_nurse)
    
    def enter_doctor_queue(self):
        self._enter_doctor_queue_time = SimClasses.Clock

    def get_type(self) -> str:
        return "transplant"