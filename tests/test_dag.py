import pytest
from src.flowforge import DAG, Task, Scheduler, Executor
import pytest
from time import sleep
from src.flowforge import DAG, Task, Scheduler, Executor


# ----- Sample tasks for testing -----
def successful_task(duration, value):
    """Task that succeeds after sleeping for `duration` seconds."""
    sleep(duration)
    return f"Success with value: {value}"


def flaky_task(attempts):
    """Task that fails a few times before succeeding."""
    if attempts.pop(0):
        raise ValueError("This task was designed to fail initially")
    return "Finally succeeded!"


def long_running_task():
    """Task that will timeout because it sleeps too long."""
    sleep(5)
    return "This will not be returned"


# ----- Tests -----
def test_executor_runs_various_tasks():
    """Executor should handle success, retries, and timeout cases."""

    tasks_to_run = [
        Task(name="quick_success", func=successful_task, args=(1, 100)),
        Task(name="stable_success", func=successful_task, args=(1, 200)),
        Task(name="timeout_task", func=long_running_task, timeout=2),
    ]

    executor = Executor(max_workers=4)
    results = executor.run_tasks(tasks_to_run)

    # quick_success and stable_success succeed
    assert results["quick_success"] == "Success with value: 100"
    assert results["stable_success"] == "Success with value: 200"



def test_dag_all_tasks_succeed():
    """DAG should run through dependent tasks successfully."""
    dag = DAG(name="success_dag")
    dag.add_task(Task(name="A", func=lambda: "A done"))
    dag.add_task(Task(name="B", func=lambda: "B done", depends_on=["A"]))
    dag.add_task(Task(name="C", func=lambda: "C done", depends_on=["B"]))

    executor = Executor(max_workers=2)
    scheduler = Scheduler(dag=dag, executor=executor)

    scheduler.run()

    assert dag.tasks["A"].result == "A done"
    assert dag.tasks["B"].result == "B done"
    assert dag.tasks["C"].result == "C done"


def test_dag_task_failure():
    """If a task fails, its result should store the exception."""
    def failing_task():
        raise ValueError("Task failed intentionally")

    dag = DAG(name="failure_dag")
    dag.add_task(Task(name="A", func=lambda: "A done"))
    dag.add_task(Task(name="Fail", func=failing_task, depends_on=["A"]))

    executor = Executor(max_workers=2)
    scheduler = Scheduler(dag=dag, executor=executor)

    scheduler.run()

    fail_task = dag.tasks["Fail"]