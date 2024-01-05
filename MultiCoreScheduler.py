from algorithm.schedule_algorithm import ScheduleAlgorithm
from task import Task, Priority
from Processor import Processor


class MultiCoreScheduler:
    def __init__(
        self,
        algorithm: ScheduleAlgorithm,
        task_list: list,
        num_processors: int = 8,
    ) -> None:
        self.algorithm: ScheduleAlgorithm = algorithm
        self.starting_task_list = task_list
        self.task_list = task_list
        self.processors = [Processor(i) for i in range(num_processors)]
        self.timer = -1
        self.num_done_tasks = 0
        self.num_expired_tasks = 0

    def run(self):
        print(f"Running {self.algorithm}")
        expired_tasks = set()

        while True:
            # next time unit
            self.timer += 1
            self.update_task_list()

            # remove outed tasks
            self.num_expired_tasks += len(
                [i for i in self.task_list if i.is_expired(self.timer)]
            )
            self.task_list = [i for i in self.task_list if not i.is_expired(self.timer)]

            # break if everything is finished
            if len(self.task_list) == 0 and len([j for j in self.processors if j.is_busy()]) == 0:
                break

            # select task
            task_list = self.algorithm.get_task_list(self.task_list)

            # Assign tasks to non busy schedulers
            non_busy_processors = [j for j in self.processors if not j.is_busy()]
            for idx, i in enumerate(non_busy_processors):
                if len(task_list) > idx:
                    i.assign_task(task_list[idx])
                    self.task_list.remove(i.assigned_task)

            # run assigned task
            busy_processors = [j for j in self.processors if j.is_busy()]
            for proc in busy_processors:
                print(f"Doing task: {proc.assigned_task} on processor {proc}")
                proc.run()

                if proc.assigned_task.is_expired(self.timer):
                    self.num_expired_tasks += 1
                    proc.task_done()

                # remove finished task from processor and queue
                elif proc.assigned_task.is_done():
                    self.num_done_tasks += 1
                    proc.task_done()

        print(f"Done EDF in {self.timer} time unit")
        print(f"Number of done tasks: {self.num_done_tasks}")
        print(f"Number of Expired Tasks: {self.num_expired_tasks}")

    def update_task_list(self):
        if self.timer == 5:
            self.task_list.append(Task(10, 2, Priority.LOW, activation_time=5))
