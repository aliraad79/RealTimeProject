from enum import Enum


class Processor:
    def __init__(self, name) -> None:
        self.name = name
        self.state: ProcessorState = ProcessorState.IDLE
        self.assigned_task = None

    def is_busy(self):
        return self.state == ProcessorState.BUSY

    def assign_task(self, task):
        self.assigned_task = task
        self.state = ProcessorState.BUSY

    def task_done(self):
        self.assigned_task = None
        self.state = ProcessorState.IDLE

    def run(self):
        self.assigned_task.run()

    def __repr__(self) -> str:
        return str(self.name)


class ProcessorState(Enum):
    BUSY = 0
    IDLE = 1
