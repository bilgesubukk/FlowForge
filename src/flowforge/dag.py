from typing import List, Dict
from collections import defaultdict

from .task import Task


class DAG:
    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)

    def add_task(self, task: Task):
        self.tasks[task.name] = task
        if task.depends_on is not None:
            for dep in task.depends_on:
                self.dependency_graph[dep].append(task.name)

    def get_independent_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if not t.depends_on]
