from task import Task
from algorithm.edf import EDF
from algorithm.wfd import WFD
from algorithm.ffd import FFD

from uunifast import generate_task_set

num_processes = 8
utilization = num_processes * 0.5
num_tasks = 20  # TODO
num_sets = 1
hc_to_lc_ratio = 1 / 0.5
task_sets = generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio)


for tasks in task_sets:
    print(f"For task set : {tasks}")
    WFD(num_processes, tasks)
    FFD(num_processes, tasks)
    WFD(num_processes, tasks, advance_mode=True)
    FFD(num_processes, tasks, advance_mode=True)
    
