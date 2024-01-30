from .schedule_algorithm import ScheduleAlgorithm

class EDF(ScheduleAlgorithm):
    def get_task_list(self, task_list: list):
        return sorted(task_list, key=lambda x: x.deadline)

    def get_overrun_task_list(self, task_list: list):
        task_list = [task for task in task_list if task.is_high_priority()]
        return sorted(task_list, key=lambda x: x.deadline)

    def __repr__(self) -> str:
        return "EDF"
