from uuid import uuid4
from enum import Enum


class Priority(Enum):
    LOW = 0
    HIGH = 1


class Task:
    def __init__(
        self, executation_time, deadline, utilization, priority: Priority, tmr_group=None
    ) -> None:
        self.id = uuid4()
        self.priority = priority
        self.deadline = deadline
        self.utilization = utilization
        self.executation_time = executation_time
        self.remaining_executation_time = executation_time
        self.tmr_group = tmr_group
        self.result = False

    def run(self, unit=1):
        self.remaining_executation_time -= unit

    def is_done(self):
        return self.remaining_executation_time == 0

    def is_expired(self, current_time):
        return self.deadline <= current_time
    
    def is_high_priority(self):
        return self.priority == Priority.HIGH
    
    def get_result(self):
        return (self.tmr_group, self.is_done())

    def __str__(self) -> str:
        return f"Task<{str(self.id)[:5]}, utilization={self.utilization}>"

    def __repr__(self) -> str:
        return self.__str__()
