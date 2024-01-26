from task import Task
from algorithm.schedule_algorithm import ScheduleAlgorithm
from algorithm.assign_algorithm import AssignAlgorithm
from math import floor
import numpy as np


class Processor:
    def __init__(
        self,
        algorithm: ScheduleAlgorithm,
        assign_algorithm: AssignAlgorithm,
        tasks: list[Task],
    ) -> None:
        self.tasks: list[Task] = []
        self.initial_task_length = 0
        self.algorithm: ScheduleAlgorithm = algorithm
        self.assign_algorithm = assign_algorithm

        self.time_step = 0.1

        self.tasks = [i for i in tasks]  # Copy
        self.initial_task_length = len(self.tasks)
        self.initial_low_priory_task_length = len(
            [i for i in self.tasks if not i.is_high_priority()]
        )

    def run(self):
        self.tasks = self.algorithm.get_task_list(self.tasks)
        self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)
        longest_task = floor(max([i.deadline for i in self.tasks]) + 1)

        done_tasks = []
        overdue_tasks = []

        for time in np.arange(
            self.time_step, longest_task + self.time_step, self.time_step
        ):
            self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)

            for _, tasks in self.tasks_dict.items():
                for task in tasks:
                    task.run(self.time_step)
                    if task.is_done():
                        done_tasks.append(task)
                    elif task.is_overdue(time):
                        overdue_tasks.append(task)

            self.tasks = [
                i for i in self.tasks if not ((i in done_tasks) or (i in overdue_tasks))
            ]
            self.tasks = self.algorithm.get_task_list(self.tasks)

        # Reporting parameters
        completation_rate = len(done_tasks) / self.initial_task_length
        Qos = (
            len([i for i in done_tasks if not i.is_high_priority()])
            / self.initial_low_priory_task_length
        )

        return (completation_rate, Qos)
