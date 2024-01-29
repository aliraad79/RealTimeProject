from abc import ABC
from task import *


class AssignAlgorithm(ABC):
    def __init__(self, num_processor, print_mode=False) -> None:
        super().__init__()
        self.num_processor = num_processor
        self.print_mode = print_mode

    def get_task_map(self, task_list):
        ...
