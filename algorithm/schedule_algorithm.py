from abc import ABC
from task import *


class ScheduleAlgorithm(ABC):
    def get_task_list(self, task_list):
        ...

    def get_overrun_task_list(self, task_list):
        ...
