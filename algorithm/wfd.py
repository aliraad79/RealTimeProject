from task import Task
from collections import defaultdict


def WFD(number_of_processor, task_list: list, advance_mode=False):
    sorted_tasks:list[Task] = sorted(task_list, key=lambda x: x.utilization, reverse=True)

    assigned_processes = {i: 1 for i in range(number_of_processor)}
    allocation = defaultdict(list)
    for task_idx, task in enumerate(sorted_tasks):
        worst_inx = -1
        for j in range(number_of_processor):
            if not advance_mode:
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
            allocation[worst_inx].append(task_idx)
            assigned_processes[worst_inx] -= task.utilization

    if advance_mode:
        print("Allocation with advance WFD:")
    else:
        print("Allocation with WFD:")
    print("processor -> task utilizations")
    for process_idx, choiced_task_list in allocation.items():
        print(f"{process_idx} -> {[task_list[i] for i in choiced_task_list]}")
