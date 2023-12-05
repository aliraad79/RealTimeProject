from abc import ABC
from task import Task


class ScheduleAlgorithm(ABC):
    def get_task_list(self, task_list:list[Task]) -> list[Task]:
        ...
