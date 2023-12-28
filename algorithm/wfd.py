from task import Task
from collections import defaultdict


def WFD(number_of_processor, task_list: list[Task]):
    sorted_tasks = sorted(task_list, key=lambda x: x.utilization, reverse=True)

    assigned_processes = {i: 1 for i in range(number_of_processor)}
    allocation = defaultdict(list)
    for task_idx, task in enumerate(sorted_tasks):
        worst_inx = -1
        for j in range(number_of_processor):
            if assigned_processes[j] > task.utilization:
                if worst_inx == -1:
                    worst_inx = j
                elif assigned_processes[worst_inx] < assigned_processes[j]:
                    worst_inx = j

        if worst_inx != -1:
            allocation[worst_inx].append(task_idx)
            assigned_processes[worst_inx] -= task.utilization

    print("Allocation with WFD:")
    print("processor -> task utilizations")
    for process_idx, choiced_task_list in allocation.items():
        print(
            f"{process_idx} -> {[task_list[i] for i in choiced_task_list]}"
        )
