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
num_sets = 10
hc_to_lc_ratio = 1 / 0.5

print_phase_one_result = False
print_phase_two_result = False

tmr_manager = TMRManager()
task_sets = generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio)
tasks_with_tmr_applied = tmr_manager.apply_tmr_to_taskset(task_sets)

if print_phase_one_result:
    for tasks in tasks_with_tmr_applied:
        print(
            f"For task set : {[(task.id, task.priority.name, task.utilization) for task in tasks]}"
        )
        WFD(num_processes, print_phase_one_result, False).get_task_map(tasks)
        FFD(num_processes, print_phase_one_result, False).get_task_map(tasks)
        WFD(num_processes, print_phase_one_result, True).get_task_map(tasks)
        FFD(num_processes, print_phase_one_result, True).get_task_map(tasks)

task_results = []
for task_set in tasks_with_tmr_applied:  # Iterate over each set of TMR tasks
    for task in task_set:  # Iterate over each task in the set
        task_results.append(task.get_result())
final_results = tmr_manager.perform_majority_voting(task_results)
if print_phase_one_result:
    print("Final Results after Majority Voting:", final_results)


results = []
for tasks in tasks_with_tmr_applied:
    processor = Processor(
        EDF(), WFD(num_processes, print_mode=False, advance_mode=False)
    )
    processor.add_tasks(tasks)
    result = processor.run()
    results.append(result)


df = pd.DataFrame(data=results, columns=["Completation_rate", "Qos"])

if print_phase_two_result:
    for completation_rate, qos in results:
        print("Completetion Rate: ", completation_rate)
        print("Completed Low Priority Tasks(Quality of service): ", qos)

fig, ax = plt.subplots(ncols=2)

ax[0].plot(df.index, df["Completation_rate"])
ax[0].axhline(df["Completation_rate"].mean())
ax[0].set_title("Complatation Rate")

# the histogram of the data
ax[1].plot(df.index, df["Qos"])
ax[1].axhline(df["Qos"].mean())
ax[1].set_title("Quality of service")

plt.show()
