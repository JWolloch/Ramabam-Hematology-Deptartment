from queueing_policy import QueueingPolicy
from python_sim import SimClasses
from python_sim.SimClasses import FIFOQueue
from simulation import Nurse

class SeparateQueuesPolicy(QueueingPolicy):
    def __init__(self, nurses: list[Nurse]):
        super().__init__(nurses)
        self.nurses_dict = {nurse.name: nurse for nurse in nurses}
        self.queues = {nurse.name: FIFOQueue() for nurse in nurses}

    def add_to_queue(self, patient):
        nurse_name = patient.assigned_nurse_name
        if nurse_name not in self.queues:
            raise ValueError(f"Nurse '{nurse_name}' does not exist.")
        self.queues[nurse_name].Add(patient)

    def get_next_patient(self, nurse_name):
        queue = self.queues.get(nurse_name)
        if queue and queue.NumQueue() > 0:
            return queue.Remove()
        return None

    def record_service_start(self, nurse_name, patient):
        patient.BeginServiceTime = SimClasses.Clock
