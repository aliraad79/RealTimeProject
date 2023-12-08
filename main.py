from task import Task
from algorithm.edf import EDF
from Scheduler import Scheduler
from uunifast import generate_task_set
from MultiCoreScheduler import MultiCoreScheduler

utilization = 4
num_tasks = 5
num_sets = 1
hc_to_lc_ratio = 1 / 0.5
task_sets = generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio)
print(task_sets)

# single core
# god_class = Scheduler(EDF(), tasks)
# god_class.run()

# Multi Core
# scheduler = MultiCoreScheduler(EDF(), tasks, 8)
# scheduler.run()
