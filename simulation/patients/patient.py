from python_sim import SimClasses, SimFunctions
from abc import ABC, abstractmethod
from datetime import datetime
from numpy import random
from scipy.stats import truncnorm
from tabulate import tabulate

class Patient(SimClasses.BooleanEntity, ABC):
    '''
    Abstract class representing a patient, inheriting from SimClasses.Entity
    '''

    def __init__(self, schedule: dict[str, datetime], doctor_name: str | None,
                 probability_of_complex_patient: float,
                 probability_of_visiting_nurse: float,
                 probability_of_needing_long_blood_test: float):
        super().__init__()
        self._schedule = schedule
        self._doctor_name = doctor_name
        self._probability_of_complex_patient = probability_of_complex_patient
        self._probability_of_visiting_nurse = probability_of_visiting_nurse
        self._probability_of_needing_long_blood_test = probability_of_needing_long_blood_test
        self._complexity_level = self._determine_complexity_level()
        self._needs_long_blood_test = self._determine_if_needs_long_blood_test()

        self.condition = False    
        self._nurse_name = None
        self._visits_nurse = self._determine_if_visits_nurse()

        self._enter_q_flow_queue_time = None
        self._enter_secretary_queue_time = None
        self._enter_nurse_queue_time = None
        self._enter_doctor_queue_time = None
        self._end_of_visit_time = None
        self._nurse_service_start_time = None
        self._blood_test_retrievel_time = None
        self._doctor_service_start_time = None
        self._q_flow_service_start_time = None
        self._secretary_service_start_time = None
        
        self._arrival_time = self._set_arrival_time()
    
    def _determine_if_visits_nurse(self) -> bool:
        u = random.uniform(0, 1)
        if u < self._probability_of_visiting_nurse:
            return True
        else:
            return False
    
    def _determine_complexity_level(self) -> str:
        u = random.uniform(0, 1)
        if u < self._probability_of_complex_patient:
            return "complex"
        else:
            return "regular"
        
    def _determine_if_needs_long_blood_test(self) -> bool:
        u = random.uniform(0, 1)
        if u < self._probability_of_needing_long_blood_test:
            return True
        else:
            return False
    
    @abstractmethod
    def get_type(self) -> str:
        raise NotImplementedError("Subclasses must implement this method")
    
    def _set_arrival_time(self) -> float:
        mean = self._schedule['arrival_time']
        std = 10 # range around schedule arrival time is 30. we use std of ten to get a normal distribution with range of 3 std in both directions
        lower = mean - 3 * std
        upper = mean + 3 * std
        a, b = (lower - mean) / std, (upper - mean) / std
        dist = truncnorm(a, b, loc=mean, scale=std)
        return dist.rvs(1)[0]
    
    def schedule_arrival(self, calendar: SimClasses.EventCalendar):
        SimFunctions.SchedulePlus(calendar, f"q_flow_station_start_of_waiting", self._arrival_time, self)


    def enter_q_flow_queue(self, clock: float):
        self._enter_q_flow_queue_time = clock

    def q_flow_service_start(self, clock: float):
        self._q_flow_service_start_time = clock

    def enter_secretary_queue(self, clock: float):
        self._enter_secretary_queue_time = clock

    def secretary_service_start(self, clock: float):
        self._secretary_service_start_time = clock
    
    def set_nurse_name(self, nurse_name: str):
        self._nurse_name = nurse_name

    def enter_nurse_queue(self, clock: float):
        self._enter_nurse_queue_time = clock
    
    def nurse_service_start(self, clock: float):
        self._nurse_service_start_time = clock

    @abstractmethod
    def enter_doctor_queue(self, clock: float):
        raise NotImplementedError("Subclasses must implement this method")        
    
    def receive_blood_test_results(self, clock: float):
        self._blood_test_retrievel_time = clock
        self.condition = True

    def end_visit(self, clock: float):
        self._end_of_visit_time = clock

    def calculate_total_visit_time(self) -> float:
        return self._end_of_visit_time - self._arrival_time
    
    def set_scheduled_arrival_time(self, new_arrival_time: float):
        self._schedule['arrival_time'] = new_arrival_time
        self._arrival_time = self._set_arrival_time()

#########################
##### Helper Methods#####
#########################

    def print_schedule(self):
        headers = ["Stage", "Scheduled Time", "Actual Time"]
        rows = [
            ["Arrival", self._schedule.get("arrival_time"), f"{self._arrival_time:.2f}"],
            ["Q-Flow Queue Entry", "-", self._enter_q_flow_queue_time],
            ["Secretary Queue Entry", "-", self._enter_secretary_queue_time],
            ["Nurse Queue Entry", "-", self._enter_nurse_queue_time if self._visits_nurse else "N/A"],
            ["Doctor Queue Entry", "-", self._enter_doctor_queue_time],
            ["End of Visit", "-", self._end_of_visit_time],
        ]
        print(f"\nPatient Schedule Summary — Doctor: {self.doctor_name}, Complexity: {self.complexity_level}, Visits Nurse: {self.visits_nurse}")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
######################
##### Properties #####
######################

    @property
    def enter_q_flow_queue_time(self) -> float | None:
        return self._enter_q_flow_queue_time
    
    @property
    def q_flow_service_start_time(self) -> float | None:
        return self._q_flow_service_start_time

    @property
    def enter_secretary_queue_time(self) -> float | None:
        return self._enter_secretary_queue_time

    @property
    def secretary_service_start_time(self) -> float | None:
        return self._secretary_service_start_time
    
    @property
    def enter_nurse_queue_time(self) -> float | None:
        return self._enter_nurse_queue_time if self._visits_nurse else None
    
    @property
    def nurse_service_start_time(self) -> float | None:
        return self._nurse_service_start_time if self._visits_nurse else None

    @property
    def nurse_name(self) -> str:
        if self._nurse_name is None:
            return "N/A"
        return self._nurse_name

    @property
    def enter_doctor_queue_time(self) -> float | None:
        return self._enter_doctor_queue_time 

    @property
    def end_of_visit_time(self) -> float | None:
        return self._end_of_visit_time
    
    @property
    def complexity_level(self) -> str:
        return self._complexity_level
    
    @property
    def visits_nurse(self) -> bool:
        return self._visits_nurse
    
    @property
    def left_department(self) -> bool:
        return self._end_of_visit_time is not None
    
    @property
    def doctor_name(self) -> str:
        return self._doctor_name
    
    @property
    def arrival_time(self) -> float:
        return self._arrival_time
    
    @property
    def scheduled_arrival_time(self) -> float:
        return self._schedule.get("arrival_time")
    
    @property
    def needs_long_blood_test(self) -> bool:
        return self._needs_long_blood_test
    
    @property
    def blood_test_retrievel_time(self) -> bool:
        return self._blood_test_retrievel_time

    @property
    def scheduled_nurse_consultation_time_vs_actual_nurse_consultation_time(self) -> float:
        if self._visits_nurse:
            return self._nurse_service_start_time - self.scheduled_arrival_time
        else:
            return None