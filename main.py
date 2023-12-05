from task import Task
from edf import EDF
from task_generation import DummyTaskGenerator

tasks = [Task(6, 2), Task(5, 3), Task(5, 3)]

tasks_generator = DummyTaskGenerator(tasks)
edf = EDF(tasks_generator)
edf.run()
