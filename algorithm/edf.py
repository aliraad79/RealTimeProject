from .schedule_algorithm import ScheduleAlgorithm
from task import Task


class EDF(ScheduleAlgorithm):
    def get_task_list(self, task_list: list):
        return sorted(task_list, key=lambda x: x.deadline)

    def __repr__(self) -> str:
        return "EDF"
