# tmr.py
from task import Task, Priority
from collections import defaultdict

class TMRManager:
    def __init__(self):
        self.tmr_group_id = 1

    def apply_tmr_to_taskset(self, task_sets:list[list[Task]]) -> list[list[Task]]:
        tmr_task_sets = []
        for task_set in task_sets:  # Expecting task_sets to be a list of lists
            tmr_task_set = []
            for task in task_set:
                if task.priority == Priority.HIGH:
                    # Create three copies of each task with the same tmr_group identifier
                    for _ in range(3):
                        tmr_task = Task(task.executation_time, task.deadline, task.utilization, task.priority, tmr_group=self.tmr_group_id)
                        tmr_task_set.append(tmr_task)
                    self.tmr_group_id += 1  # Increment the identifier for the next group
                else:
                    tmr_task_set.append(task)
            tmr_task_sets.append(tmr_task_set)
        return tmr_task_sets

    def perform_majority_voting(self, task_results):
        """
        Perform majority voting on the results of tasks.
        task_results should be a list of tuples (tmr_group_id, result)
        """
        vote_counts = defaultdict(lambda: defaultdict(int))
        for group_id, result in task_results:
            vote_counts[group_id][result] += 1

        final_results = {}
        for group_id, votes in vote_counts.items():
            final_results[group_id] = max(votes, key=votes.get)  # Get the result with the most votes

        return final_results

# Example usage of the class
# tmr_manager = TMRManager()
# tmr_tasks = tmr_manager.apply_tmr_to_taskset(original_task_set)
# ... execute tasks ...
# final_results = tmr_manager.perform_majority_voting(task_results)
