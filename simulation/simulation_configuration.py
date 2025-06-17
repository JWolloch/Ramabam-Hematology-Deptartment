from dataclasses import dataclass

@dataclass
class SimulationConfiguration:
    num_epochs: int = 100
    num_epochs_test: int = 5
    personalize_schedule: bool = False