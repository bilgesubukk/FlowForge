from typing import Callable, List, Dict, Any
from collections import defaultdict

class Task:
    def __init__(self, name: str, func: Callable, depends_on: List[str] = None):
        self.name = name
        self.func = func
        self.depends_on = depends_on or []
        self.result = None

class DAG:
    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)

    def add_task(self, task: Task):
        self.tasks[task.name] = task
        for dep in task.depends_on:
            self.dependency_graph[dep].append(task.name)

    def get_independent_tasks(self) -> List[Task]:
        """Return tasks that have no dependencies or whose dependencies are done."""
        return [t for t in self.tasks.values() if not t.depends_on]
