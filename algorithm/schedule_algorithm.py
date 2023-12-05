from abc import ABC
from task_generation.task_generation import TaskGenerator


class ScheduleAlgorithm(ABC):
    def __init__(self, task_generator) -> None:
        self.task_generator: TaskGenerator = task_generator

    def run(self):
        ...
