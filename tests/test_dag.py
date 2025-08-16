import pytest
from src.flowforge import DAG, Task, Scheduler, Executor

# ----- Sample tasks for testing -----
def task_a():
    return "A done"

def task_b():
    return "B done"

def task_c():
    return "C done"

def failing_task():
    raise ValueError("Task failed intentionally")


# ----- Test DAG execution -----
def test_dag_runs_successfully():
    dag = DAG(name="test_dag_success")
    dag.add_task(Task(name="A", func=task_a))
    dag.add_task(Task(name="B", func=task_b, depends_on=["A"]))
    dag.add_task(Task(name="C", func=task_c, depends_on=["B"]))

    executor = Executor(max_workers=2)
    scheduler = Scheduler(dag=dag, executor=executor)

    # Should not raise any errors
    scheduler.run()

    # Check all tasks exist in DAG
    assert "A" in dag.tasks
    assert "B" in dag.tasks
    assert "C" in dag.tasks

def test_dag_detects_failure():
    dag = DAG(name="test_dag_failure")
    dag.add_task(Task(name="A", func=task_a))
    dag.add_task(Task(name="Fail", func=failing_task, depends_on=["A"]))

    executor = Executor(max_workers=2)
    scheduler = Scheduler(dag=dag, executor=executor)

    scheduler.run()

    fail_task = dag.tasks["Fail"]
    assert isinstance(fail_task.result, Exception)
    assert str(fail_task.result) == "Task failed intentionally"
