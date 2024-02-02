from task import Task
from algorithm.schedule_algorithm import ScheduleAlgorithm
from algorithm.assign_algorithm import AssignAlgorithm
import numpy as np
import random


class Processor:
    def __init__(
        self,
        algorithm: ScheduleAlgorithm,
        assign_algorithm: AssignAlgorithm,
        tasks,
        num_cores,
        is_overrun=False,
    ) -> None:
        self.algorithm: ScheduleAlgorithm = algorithm
        self.assign_algorithm = assign_algorithm

        self.time = 0
        self.time_step = 0.1
        self.cores = [Core(i, self.time_step) for i in range(num_cores)]

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

        # Offline phase
        self.tasks = self.algorithm.get_task_list(self.tasks)
        self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)
        for core_id, tasks_set in self.tasks_dict.items():
            self.cores[core_id].set_tasks(tasks_set)
            if sum(i.utilization for i in tasks_set) < 1:
                self.cores[core_id].make_host()

        self.initial_distributation = self.assign_algorithm.get_task_map(self.tasks)

    def run(self):
        # Online phase
        done_tasks = []

        while sum(len(i.tasks) for i in self.cores) != 0:
            self.time += self.time_step

            if self.is_overrun and self.time == self.overrun_time:
                self.reschedule(edf_vd=False)

            for core in self.cores:
                core_done_tasks = core.run(self.time)
                done_tasks.extend(core_done_tasks)

        # Reporting parameters
        completation_rate = len(done_tasks) / self.initial_task_length
        Qos = (
            len([i for i in done_tasks if not i.is_high_priority()])
            / self.initial_low_priory_task_length
        )

        return (
            completation_rate,
            Qos,
            self.initial_distributation.items(),
            self.overrun_distributation.items(),
        )

    def reschedule(self, edf_vd=True):
        if edf_vd:
            tasks = []
            for task_list in self.tasks_dict.values():
                tasks.extend(task_list)

            # Migrate
            self.tasks = self.algorithm.get_overrun_task_list(tasks)
            self.tasks_dict = self.assign_algorithm.get_task_map(self.tasks)
            for core_id, tasks_set in self.tasks_dict.items():
                self.cores[core_id].set_tasks(tasks_set)

            self.overrun_distributation = self.assign_algorithm.get_task_map(self.tasks)
        else:
            tasks = []
            for task_list in self.tasks_dict.values():
                tasks.extend(task_list)

            # Migrate
            random_cores = random.sample(range(len(self.cores)), len(self.cores) // 2)
            soft_tasks = []
            for core_id in random_cores:
                core_soft_tasks = self.cores[core_id].set_overrun()
                soft_tasks.extend(core_soft_tasks)

            host_cores = [
                i
                for i in range(len(self.cores))
                if i not in random_cores and self.cores[i].is_host
            ]
            # Best fit
            for task in soft_tasks:
                lowest_utilized_core = sorted(
                    host_cores, key=lambda x: self.cores[x].sum_util()
                )[0]

                self.cores[lowest_utilized_core].tasks.append(task)

            self.overrun_distributation = {
                core.core_number: core.tasks for core in self.cores
            }


class Core:
    def __init__(self, core_number, time_step) -> None:
        self.is_overrun = False
        self.time_step = time_step
        self.core_number = core_number
        self.is_host = False

    def set_tasks(self, tasks):
        self.tasks = tasks

    def set_overrun(self):
        self.is_overrun = True
        soft_tasks = [task for task in self.tasks if not task.is_high_priority()]
        self.tasks = [task for task in self.tasks if task.is_high_priority()]
        return soft_tasks

    def make_host(self):
        self.is_host = True

    def sum_util(self):
        return sum(i.utilization for i in self.tasks)

    def run(self, time):
        done_tasks = []
        overdue_tasks = []

        for task in self.tasks:
            task.run(self.time_step, self.is_overrun)
            if task.is_done():
                done_tasks.append(task)
            elif task.is_overdue(time):
                overdue_tasks.append(task)

        for task in done_tasks:
            self.tasks.remove(task)
        for task in overdue_tasks:
            self.tasks.remove(task)

        return done_tasks

    def __repr__(self) -> str:
        return f"Core<{self.sum_util()}>"
