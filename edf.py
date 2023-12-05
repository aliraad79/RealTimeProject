from task import Task


def run_edf(task_list: list[Task]):
    print("Running EDF")
    timer = -1
    expired_tasks = set()
    ready_tasks = sorted(task_list, key=lambda x: x.deadline)

    while True:
        # next time unit
        timer += 1
        # remove outed tasks
        for i in ready_tasks:
            if i.is_expired(timer):
                expired_tasks.add(i)
        for i in expired_tasks:
            if i in ready_tasks:
                ready_tasks.remove(i)
            
        # break if everything is finished
        if len(ready_tasks) == 0:
            break
        # select task
        selected_task = ready_tasks[0]

        if selected_task.is_done():
            ready_tasks.remove(selected_task)
            continue

        print("Doing task: ", selected_task)
        selected_task.run()

    print(f"Done EDF in {timer} time unit")
    print(f"Expired Tasks: {expired_tasks}")
