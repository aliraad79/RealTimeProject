from uuid import uuid4
from enum import Enum


class Priority(Enum):
    LOW = 0
    HIGH = 1


class Task:
    def __init__(
        self,
        executation_time,
        deadline,
        priority: Priority,
        activation_time: int = 0,
    ) -> None:
        self.id = uuid4()
        self.priority = priority
        self.activation_time = activation_time
        self.deadline = deadline
        self.executation_time = executation_time
        self.remaining_executation_time = executation_time

    def run(self, unit=1):
        self.remaining_executation_time -= unit

    def is_done(self):
        return self.remaining_executation_time == 0

    def is_expired(self, current_time):
        return self.deadline <= current_time

    def __str__(self) -> str:
        return f"Task<deadline={self.deadline}, executation_time={self.remaining_executation_time}, Priority={self.priority}>"

    def __repr__(self) -> str:
        return self.__str__()
