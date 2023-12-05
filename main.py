from task import Task
from algorithm.edf import EDF
from Scheduler import Scheduler
from MultiCoreScheduler import MultiCoreScheduler

tasks = [
    Task(6, 2),
    Task(5, 3),
    Task(5, 3),
    Task(5, 3),
    Task(5, 3),
    Task(5, 3),
    Task(5, 3),
    Task(5, 3),
    Task(5, 3),
]

# single core
# god_class = Scheduler(EDF(), tasks)
# god_class.run()

# Multi Core
scheduler = MultiCoreScheduler(EDF(), tasks, 8)
scheduler.run()
