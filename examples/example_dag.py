from time import sleep
from src.flowforge import DAG, Task, Executor, get_logger

logger = get_logger("example_dag")


# ----- Define your tasks -----
def successful_task(duration, value):
    """A sample task that succeeds after a delay."""
    print(f"  -> Running '{successful_task.__name__}' for {duration}s...")
    sleep(1)
    return f"Success with value: {value}"


def failing_task(attempt_to_succeed):
    """A sample task that fails a few times before succeeding."""
    print(f"  -> Running '{failing_task.__name__}'...")
    sleep(1)
    if attempt_to_succeed.pop(0):
        raise ValueError("This task was designed to fail initially")
    return "Finally succeeded!"


def long_running_task():
    """A sample task that will be terminated by a timeout."""
    print(f"  -> Running '{long_running_task.__name__}' which will time out...")
    sleep(2)
    return "This will not be returned"


# ----- Build DAG -----
dag = DAG(name="example_etl")

fail_control = [True, True, False]  # Fails twice, succeeds on the third try

# Define a list of tasks with different configurations
tasks_to_run = [
    Task(name="quick_success", func=successful_task, args=(1, 100)),
    Task(name="stable_success", func=successful_task, args=(2, 200)),
    Task(name="flaky_task_with_retries", func=failing_task, args=(fail_control,), retries=2),
    Task(name="timeout_task", func=long_running_task, timeout=3),
]

print("Starting task execution...\n")
executor = Executor(max_workers=4)
final_results = executor.run_tasks(tasks_to_run)

print("\n--- Final Results ---")
for name, result in final_results.items():
    if isinstance(result, Exception):
        print(f"Task '{name}': Failed with error: {result}")
    else:
        print(f"Task '{name}': Succeeded with result: '{result}'")
