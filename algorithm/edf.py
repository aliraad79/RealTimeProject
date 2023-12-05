from .schedule_algorithm import ScheduleAlgorithm
from task import Task


class EDF(ScheduleAlgorithm):
    def choose_task(self, task_list: list[Task]):
        return sorted(task_list, key=lambda x: x.deadline)[0]

    def __repr__(self) -> str:
        return "EDF"
