from patients.patient import Patient
from datetime import datetime
from python_sim import SimClasses

class TransplantPatient(Patient):
    def __init__(self, schedule: dict[str, datetime], doctor_name: str | None,
                 probability_of_complex_patient: float,
                 probability_of_visiting_nurse: float,
                 probability_of_needing_long_blood_test: float):
        super().__init__(schedule, doctor_name, probability_of_complex_patient, probability_of_visiting_nurse, probability_of_needing_long_blood_test)
        self._doctor_service_start_time = None
    def enter_doctor_queue(self, clock: float):
        self._enter_doctor_queue_time = clock

    def doctor_service_start(self, clock: float):
        self._doctor_service_start_time = clock

    def get_type(self) -> str:
        return "transplant"
    
    @property
    def scheduled_doctor_consultation_time_vs_actual_doctor_consultation_time(self) -> float:
        return self._doctor_service_start_time - self._schedule.get("doctor_consultation_time")
    
    @property
    def doctor_service_start_time(self) -> float | None:
        return self._doctor_service_start_time
    
    @property
    def scheduled_doctor_consultation_time(self) -> float:
        return self._schedule.get("doctor_consultation_time")