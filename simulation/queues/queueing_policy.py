from abc import ABC, abstractmethod
from typing import List
from simulation import Nurse

class QueueingPolicy(ABC):
    def __init__(self, nurses: List[Nurse]):
        self.nurses = nurses

    @abstractmethod
    def add_to_queue(self, patient):
        pass

    @abstractmethod
    def get_next_patient(self, nurse_name: str):
        pass

    @abstractmethod
    def record_service_start(self, nurse_name: str, patient):
        pass
