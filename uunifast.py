import random
import numpy as np
from task import Task, Priority


def trunc(x, p):
    return int(x * 10**p) / float(10**p)


def generate_random_periods_uniform(
    num_periods: int,
    num_sets: int,
    min_period: float,
    max_period: float,
    round_to_int: bool = False,
):
    """
    Generate a list of num_sets sets containing each num_periods random periods using a uniform distribution.
    Args:
        - num_periods: The number of periods in a period set.
        - num_sets: Number of sets to generate.
        - min_period: Minimum period value.
        - max_period: Maximum period value.
        - round_to_int: Whether to round the generated periods to integers.
    """
    periods = np.random.uniform(
        low=min_period, high=max_period, size=(num_sets, num_periods)
    )

    if round_to_int:
        periods = np.rint(periods).tolist()
    else:
        periods = periods.tolist()

    return periods


def generate_uunifast(nsets: int, u: float, num_tasks: int):
    sets = []
    while len(sets) < nsets:
        utilizations = []
        sumU = u
        for i in range(1, num_tasks):
            nextSumU = sumU * random.random() ** (1.0 / (num_tasks - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(sumU)
        
        # if all(ut <= 1 for ut in utilizations):
        sets.append(utilizations)

    return sets


def generate_tasksets(utilizations, periods):
    """
    Take a list of task utilization sets and a list of task period sets and
    return a list of couples (c, p) sets. The computation times are truncated
    at a precision of 10^-10 to avoid floating point precision errors.
    Args:
        -   utilizations : The list of task utilization sets.
        -   periods : The list of task period sets.
    Returns:
        For the above example, it returns:
            [[(30.0, 100), (20.0, 50), (800.0, 1000)],
             [(20.0, 200), (450.0, 500), (5.0, 10)]]
    """

    return [
        [(trunc(ui * pi, 6), trunc(pi, 6), trunc(ui, 6)) for ui, pi in zip(us, ps)]
        for us, ps in zip(utilizations, periods)
    ]


def generate_task_set(utilization, num_tasks, num_sets, hc_to_lc_ratio, wcet_high_coeficcient):
    periods = generate_random_periods_uniform(num_tasks, num_sets, 5, 10)
    uunifast = generate_uunifast(num_sets, utilization, num_tasks)
    task_sets = generate_tasksets(uunifast, periods)

    final_task_set = []
    for set in task_sets:
        task_list = []
        for idx, task in enumerate(set):
            priority = Priority.HIGH if idx % hc_to_lc_ratio == 0 else Priority.LOW
            if priority == Priority.HIGH:
                task_list.append(Task(task[0], task[1], task[2], priority, task[0] * wcet_high_coeficcient))
            else:
                task_list.append(Task(task[0], task[1], task[2], priority))
        final_task_set.append(task_list)

    return final_task_set
