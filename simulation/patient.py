from pythonSim.SimClasses import Entity
from numpy import random


class Patient(Entity):
    def __init__(self, id, arrival_time, patient_type, probability_of_needing_a_test, probability_of_regular_test, probability_of_complex_test):
        super().__init__(id, arrival_time)
        self.patient_type = patient_type
        self.needs_test = self.calculate_needs_test()
        self.test_type = self.calculate_test_type() if self.needs_test else None

    def calculate_needs_test(self):
        return random.uniform(0, 1) < self.probability_of_needing_a_test

    def calculate_test_type(self):
        u = random.uniform(0, 1)
        if u < self.probability_of_regular_test:
            return "regular"
        else:
            return "complex"


