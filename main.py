import pandas as pd
import matplotlib.pyplot as plt
from algorithm.edf import EDF
from algorithm.wfd import WFD
from algorithm.ffd import FFD

from uunifast import generate_task_set
from tmr import TMRManager
from processor import Processor

num_processes = 16
utilization = num_processes * 0.75
num_tasks = 20
num_sets = 200
hc_to_lc_ratio = 1 / 0.5
wcet_high_coeficcient = 1.2


tmr_manager = TMRManager()
task_sets = generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio, wcet_high_coeficcient)
tasks_with_tmr_applied = tmr_manager.apply_tmr_to_taskset(task_sets)

task_results = []
for task_set in tasks_with_tmr_applied:  # Iterate over each set of TMR tasks
    for task in task_set:  # Iterate over each task in the set
        task_results.append(task.get_result())
final_results = tmr_manager.perform_majority_voting(task_results)

results = []
for row, tasks in enumerate(tasks_with_tmr_applied):
    processor = Processor(
        EDF(), WFD(num_processes, print_mode=False, advance_mode=False), tasks, num_processes, is_overrun=True
    )
    result = processor.run()
    results.append(result)


df = pd.DataFrame(data=results, columns=["Completation_rate", "Qos", "task_distributation", "Overrun_distribution"])
df['task_distributation'].to_csv("./schedule.csv")
df['Overrun_distribution'].to_csv("./overrun_schedule.csv")

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