from .dag import DAG
from .executor import Executor

class Scheduler:
    def __init__(self, dag: DAG, executor: Executor):
        self.dag = dag
        self.executor = executor

    def run(self):
        completed = set()
        while len(completed) < len(self.dag.tasks):
            ready_tasks = [
                t for t in self.dag.tasks.values()
                if t.name not in completed and all(dep in completed for dep in t.depends_on)
            ]
            if not ready_tasks:
                raise RuntimeError("Cyclic dependency detected or no tasks ready")
            results = self.executor.run_tasks(ready_tasks)
            for task_name in results:
                completed.add(task_name)
