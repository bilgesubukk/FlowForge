from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
from .logger import get_logger

logger = get_logger(__name__)

class Executor:
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers

    def run_tasks(self, tasks: list):
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_task = {pool.submit(task.func): task for task in tasks}
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    task.result = result
                    results[task.name] = result
                    logger.info(f"Task '{task.name}' completed with result: {result}")
                except Exception as e:
                    task.result = e
                    results[task.name] = e
                    logger.error(f"Task '{task.name}' failed: {e}")
        return results
