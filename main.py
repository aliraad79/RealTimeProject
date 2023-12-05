from task import Task
from algorithm.edf import EDF
from notNamedClass import Scheduler

tasks = [Task(6, 2), Task(5, 3), Task(5, 3)]

god_class = Scheduler(EDF(), tasks)
god_class.run()