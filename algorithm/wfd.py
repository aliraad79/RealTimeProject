from task import Task
from collections import defaultdict
from algorithm.assign_algorithm import AssignAlgorithm


class WFD(AssignAlgorithm):
    def __init__(self, num_processor, print_mode, advance_mode) -> None:
        super().__init__(num_processor, print_mode)
        self.advance_mode = advance_mode

    def get_task_map(self, task_list):
        sorted_tasks: list[Task] = sorted(
            task_list, key=lambda x: x.utilization, reverse=True
        )

        assigned_processes = {i: 1 for i in range(self.num_processor)}
        allocation = {i: list() for i in range(self.num_processor)}
        for task_idx, task in enumerate(sorted_tasks):
            worst_inx = -1
            for j in range(self.num_processor):
                if not self.advance_mode:
                    if assigned_processes[j] > task.utilization:
                        if worst_inx == -1:
                            worst_inx = j
                        elif assigned_processes[worst_inx] < assigned_processes[j]:
                            worst_inx = j
                else:
                    if (
                        task.is_high_priority()
                        and (assigned_processes[j] > task.utilization)
                    ) or (
                        not task.is_high_priority()
                        and ((assigned_processes[j] + 0.5) > task.utilization)
                    ):
                        if worst_inx == -1:
                            worst_inx = j
                        elif assigned_processes[worst_inx] < assigned_processes[j]:
                            worst_inx = j

            if worst_inx != -1:
                allocation[worst_inx].append(sorted_tasks[task_idx])
                assigned_processes[worst_inx] -= task.utilization

        if self.print_mode:
            if self.advance_mode:
                print("Allocation with advance WFD:")
            else:
                print("Allocation with WFD:")
            print("processor -> task utilizations")
            for process_idx, choiced_task_list in allocation.items():
                print(f"{process_idx} -> {[i for i in choiced_task_list]}")
        
        return allocation
