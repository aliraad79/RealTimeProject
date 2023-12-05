from abc import ABC
from task import Task


class ScheduleAlgorithm(ABC):
    def choose_task(self, task_list:list[Task]) -> Task:
        ...
