from task import Task
from algorithm.schedule_algorithm import ScheduleAlgorithm
from algorithm.assign_algorithm import AssignAlgorithm
import math
import numpy as np


class Processor:
    def __init__(
        self,
        algorithm: ScheduleAlgorithm,
        assign_algorithm: AssignAlgorithm,
        tasks,
        is_overrun=False,
    ) -> None:
        self.algorithm: ScheduleAlgorithm = algorithm
        self.assign_algorithm = assign_algorithm

        self.time = 0
        self.time_step = 0.1

        self.tasks = tasks
        self.initial_task_length = len(self.tasks)
        self.initial_low_priory_task_length = len(
            [i for i in self.tasks if not i.is_high_priority()]
        )
        self.host = -1
        self.is_overrun = is_overrun
        self.overrun_distributation = {}
        # select random overrun time
        if self.is_overrun:
            max_time = max([i.executation_time for i in self.tasks])
            # depend on time_step
            self.overrun_time = round(
                np.random.uniform(low=0, high=max_time, size=1)[0], 1
            )

    def run(self):
        done_tasks = []
        overdue_tasks = []

        self.tasks = self.algorithm.get_task_list(self.tasks)
        self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)
        initial_distributation = self.assign_algorithm.get_task_map(self.tasks)

        while sum(len(i) for i in self.tasks_dict.values()) != 0:
            self.time += self.time_step

            if self.is_overrun and self.time == self.overrun_time:
                self.reschedule()

            shall_removed = []

            for proc_id, tasks in self.tasks_dict.items():
                for task in tasks:
                    task.run(self.time_step, self.is_overrun)
                    if task.is_done():
                        done_tasks.append(task)
                        shall_removed.append((proc_id, task))
                    elif task.is_overdue(self.time):
                        overdue_tasks.append(task)
                        shall_removed.append((proc_id, task))

            for i in shall_removed:
                self.remove_from_task_dict(i[0], i[1])

        # Reporting parameters
        completation_rate = len(done_tasks) / self.initial_task_length
        Qos = (
            len([i for i in done_tasks if not i.is_high_priority()])
            / self.initial_low_priory_task_length
        )

        return (completation_rate, Qos, initial_distributation.items(), self.overrun_distributation.items())

    def remove_from_task_dict(self, processor_id, task):
        self.tasks_dict[processor_id].remove(task)

    def reschedule(self):
        tasks = []
        for task_list in self.tasks_dict.values():
            tasks.extend(task_list)

        self.tasks = self.algorithm.get_overrun_task_list(tasks)
        self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)
        self.overrun_distributation = self.assign_algorithm.get_task_map(self.tasks)
