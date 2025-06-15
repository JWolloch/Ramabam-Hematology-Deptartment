from patients.patient import Patient
from datetime import datetime

class OtherPatient(Patient):
    def __init__(self, schedule: dict[str, datetime], doctor_name: str | None,
                 probability_of_complex_patient: float,
                 probability_of_visiting_nurse: float,
                 probability_of_needing_long_blood_test: float):
        super().__init__(schedule, doctor_name, probability_of_complex_patient, probability_of_visiting_nurse, probability_of_needing_long_blood_test)
    
    def enter_doctor_queue(self, clock: float):
        pass

    def get_type(self) -> str:
        return "other"