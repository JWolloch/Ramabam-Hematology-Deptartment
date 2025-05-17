from queueing_policy import QueueingPolicy
from pythonSim import SimClasses, SimFunctions
from pythonSim.SimClasses import FIFOQueue
from simulation import Nurse

class SharedQueuePolicy(QueueingPolicy):
    def __init__(self, nurses: list[Nurse], preparation_time: float):
        super().__init__(nurses)
        self.shared_queue = FIFOQueue()
        self.preparation_time = preparation_time  # in minutes
        self.calendar = None  # Will be injected later

    def set_calendar(self, calendar):
        self.calendar = calendar

    def add_to_queue(self, patient):
        self.shared_queue.Add(patient)

    def get_next_patient(self, nurse_name: str = None):
        if self.shared_queue.NumQueue() > 0:
            return self.shared_queue.Remove()
        return None

    def record_service_start(self, nurse_name: str, patient):
        patient.BeginServiceTime = SimClasses.Clock

    def nurse_becomes_available(self, nurse: Nurse):
        if self.shared_queue.NumQueue() > 0:
            # Schedule nurse to begin service after the prep buffer
            SimFunctions.SchedulePlus(
                self.calendar,
                "NurseReadyToStartService",
                self.preparation_time,
                nurse
            )
