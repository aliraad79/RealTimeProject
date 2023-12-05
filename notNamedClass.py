from algorithm.schedule_algorithm import ScheduleAlgorithm
from task import Task


class Scheduler:
    def __init__(self, algorithm: ScheduleAlgorithm, task_list: list[Task]) -> None:
        self.algorithm: ScheduleAlgorithm = algorithm
        self.starting_task_list = task_list
        self.task_list = task_list

    def run(self):
        print(f"Running {self.algorithm}")
        timer = -1
        expired_tasks = set()


        while True:
            # next time unit
            timer += 1
            # remove outed tasks
            for i in self.task_list:
                if i.is_expired(timer):
                    expired_tasks.add(i)
            for i in expired_tasks:
                if i in self.task_list:
                    self.task_list.remove(i)

            # break if everything is finished
            if len(self.task_list) == 0:
                break
            # select task
            selected_task = self.algorithm.choose_task(self.task_list)

            if selected_task.is_done():
                self.task_list.remove(selected_task)
                continue

            print("Doing task: ", selected_task)
            selected_task.run()

        print(f"Done EDF in {timer} time unit")
        print(f"Expired Tasks: {expired_tasks}")