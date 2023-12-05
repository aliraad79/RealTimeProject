from abc import ABC
from task import Task


class TaskGenerator(ABC):
    def generate(self) -> list[Task]:
        ...


class DummyTaskGenerator(TaskGenerator):
    def __init__(self, task_list) -> None:
        self.task_list = task_list

    def generate(self):
        return self.task_list
