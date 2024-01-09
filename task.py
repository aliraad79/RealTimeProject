from uuid import uuid4
from enum import Enum


class Priority(Enum):
    LOW = 0
    HIGH = 1


class IDGenerator:
    _id = 0

    @classmethod
    def getID(cls):
        cls._id += 1
        return cls._id


class Task:
    def __init__(
        self,
        executation_time,
        deadline,
        utilization,
        priority: Priority,
        tmr_group=None,
    ) -> None:
        self.id = IDGenerator.getID()
        self.priority = priority
        self.deadline = deadline
        self.utilization = utilization
        self.executation_time = executation_time
        self.remaining_executation_time = executation_time
        self.tmr_group = tmr_group
        self.result = False

    def is_done(self):
        return self.remaining_executation_time <= 0

    def is_overdue(self, current_time):
        return self.deadline < self.remaining_executation_time + current_time

    def is_high_priority(self):
        return self.priority == Priority.HIGH

    def get_result(self):
        return (self.tmr_group, self.is_done())

    def run(self, step):
        self.remaining_executation_time -= step
    
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id

    def __str__(self) -> str:
        return f"Task<{self.id}, {self.priority.name}>"

    def __repr__(self) -> str:
        return self.__str__()
