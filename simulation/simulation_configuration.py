from dataclasses import dataclass

@dataclass
class SimulationConfiguration:
    num_epochs: int = 100
    num_epochs_test: int = 5

@dataclass
class HyperParameters:
    start_time: int = 30
    end_time: int = 270
    interval: int = 20
    mean_num_patients: int = 100