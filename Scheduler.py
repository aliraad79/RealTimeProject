from algorithm.schedule_algorithm import ScheduleAlgorithm
from task import Task, Priority


class Scheduler:
    def __init__(self, algorithm: ScheduleAlgorithm, task_list: list[Task]) -> None:
        self.algorithm: ScheduleAlgorithm = algorithm
        self.starting_task_list = task_list
        self.task_list = task_list
        self.timer = 0
        self.num_done_tasks = 0
        self.num_expired_tasks = 0

    def run(self):
        print(f"Running {self.algorithm}")

        while True:
            # next time unit
            self.timer += 1
            self.update_task_list()

            # remove outed tasks
            self.num_expired_tasks += len([i for i in self.task_list if i.is_expired(self.timer)])
            self.task_list = [i for i in self.task_list if not i.is_expired(self.timer)]

            # break if everything is finished
            if len(self.task_list) == 0:
                break

            # select task
            selected_task = self.algorithm.get_task_list(self.task_list)[0]

            selected_task.run()
            print("Done task: ", selected_task)

            # remove task from queue if done
            if selected_task.is_done():
                self.task_list.remove(selected_task)
                self.num_done_tasks += 1
                continue


        print(f"Done EDF in {self.timer} time unit")
        print(f"Number of done tasks: {self.num_done_tasks}")
        print(f"Number of Expired Tasks: {self.num_expired_tasks}")

    def update_task_list(self):
        if self.timer == 5:
            self.task_list.append(Task(10, 2, Priority.LOW, activation_time=5))