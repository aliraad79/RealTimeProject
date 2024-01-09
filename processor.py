from task import Task
from algorithm.schedule_algorithm import ScheduleAlgorithm
from math import floor
import numpy as np


class Processor:
    def __init__(self, num_processor, algorithm: ScheduleAlgorithm) -> None:
        self.proccesors = [Core() for i in range(num_processor)]
        self.tasks: list[Task] = []
        self.algorithm: ScheduleAlgorithm = algorithm

        self.time_step = 0.1

    def add_tasks(self, tasks: list[Task]):
        self.tasks.extend(tasks)

    def run(self):
        self.tasks = self.algorithm.get_task_list(self.tasks)
        longest_task = floor(max([i.deadline for i in self.tasks]) + 1)

        for step in np.arange(
            self.time_step, longest_task + self.time_step, self.time_step
        ):
            done_tasks = []
            for task in self.tasks:
                self.main_loop(task)
                if task.is_done():
                    done_tasks.append(task)
            self.tasks = [i for i in self.tasks if i not in done_tasks]
            self.tasks = self.algorithm.get_task_list(self.tasks)

            if len(done_tasks) != 0:
                print("Done Tasks: ", done_tasks)
                print("Tasks: ", self.tasks)

    def main_loop(self, task: Task):
        task.run(self.time_step)


class Core:
    def __init__(self) -> None:
        pass
