from task import Task
from algorithm.edf import EDF
from algorithm.wfd import WFD
from algorithm.ffd import FFD

from uunifast import generate_task_set
from tmr import TMRManager

num_processes = 8
utilization = num_processes * 0.5
num_tasks = 20  # TODO
num_sets = 1
hc_to_lc_ratio = 1 / 0.5

tmr_manager = TMRManager()
task_sets = generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio)
tmr_tasks = tmr_manager.apply_tmr_to_taskset(task_sets)

for tasks in tmr_tasks:
    print(f"For task set : {tasks}")
    WFD(num_processes, tasks)
    FFD(num_processes, tasks)
    WFD(num_processes, tasks, advance_mode=True)
    FFD(num_processes, tasks, advance_mode=True)

task_results = []
for task_set in tmr_tasks:  # Iterate over each set of TMR tasks
    for task in task_set:   # Iterate over each task in the set
        task_results.append(task.get_result())
final_results = tmr_manager.perform_majority_voting(task_results)
print("Final Results after Majority Voting:", final_results)
    
