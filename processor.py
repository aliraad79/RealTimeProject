from task import Task
from algorithm.schedule_algorithm import ScheduleAlgorithm
from algorithm.assign_algorithm import AssignAlgorithm
from math import floor
import numpy as np


class Processor:
    def __init__(
        self,
        num_processor,
        algorithm: ScheduleAlgorithm,
        assign_algorithm: AssignAlgorithm,
    ) -> None:
        self.proccesors = [Core() for i in range(num_processor)]
        self.tasks: list[Task] = []
        self.algorithm: ScheduleAlgorithm = algorithm
        self.assign_algorithm = assign_algorithm
        self.initial_task_length = 0

        self.time_step = 0.1

    def add_tasks(self, tasks: list[Task]):
        self.tasks = [i for i in tasks] # Copy
        self.initial_task_length = len(self.tasks)

    def run(self):
        self.tasks = self.algorithm.get_task_list(self.tasks)
        self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)
        longest_task = floor(max([i.deadline for i in self.tasks]) + 1)

        completed_tasks_before_deadline = []
        overdue_tasks = []

        for time in np.arange(
            self.time_step, longest_task + self.time_step, self.time_step
        ):
            done_tasks = []

            self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)

            for processor_id, tasks in self.tasks_dict.items():
                for task in tasks:
                    task.run(self.time_step)
                    if task.is_done():
                        done_tasks.append(task)
                        completed_tasks_before_deadline.append(task)
                    elif task.is_overdue(time):
                        overdue_tasks.append(task)

            # print("T",overdue_tasks)
            self.tasks = [i for i in self.tasks if i not in done_tasks]
            self.tasks = [i for i in self.tasks if i not in overdue_tasks]
            self.tasks = self.algorithm.get_task_list(self.tasks)

        print(
            "Completetion Rate: ",
            len(completed_tasks_before_deadline) / self.initial_task_length,
        )


class Core:
    def __init__(self) -> None:
        pass
