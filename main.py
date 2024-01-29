import pandas as pd
import matplotlib.pyplot as plt
from algorithm.edf import EDF
from algorithm.wfd import WFD
from algorithm.ffd import FFD

from uunifast import generate_task_set
from tmr import TMRManager
from processor import Processor

num_processes = 8
utilization = num_processes * 0.5
num_tasks = 10
num_sets = 20
hc_to_lc_ratio = 1 / 0.5


tmr_manager = TMRManager()
task_sets = generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio)
tasks_with_tmr_applied = tmr_manager.apply_tmr_to_taskset(task_sets)

task_results = []
for task_set in tasks_with_tmr_applied:  # Iterate over each set of TMR tasks
    for task in task_set:  # Iterate over each task in the set
        task_results.append(task.get_result())
final_results = tmr_manager.perform_majority_voting(task_results)

results = []
for tasks in tasks_with_tmr_applied:
    processor = Processor(
        EDF(), WFD(num_processes, print_mode=False, advance_mode=False), tasks
    )
    result = processor.run()
    results.append(result)


df = pd.DataFrame(data=results, columns=["Completation_rate", "Qos", "task_distributation"])
df['task_distributation'].to_csv("./schedule.csv")

fig, ax = plt.subplots(ncols=2)

ax[0].plot(df.index, df["Completation_rate"])
ax[0].axhline(df["Completation_rate"].mean())
ax[0].set_title("Complatation Rate")

# the histogram of the data
ax[1].plot(df.index, df["Qos"])
ax[1].axhline(df["Qos"].mean())
ax[1].set_title("Quality of service")

plt.show()

df['task_distributation'].to_csv("./schedule.csv")