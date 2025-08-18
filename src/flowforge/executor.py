from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from tqdm import tqdm

from .task import Task
from .logger import get_logger

logger = get_logger(__name__)

class Executor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def run_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        results = {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            tasks_to_process = list(tasks)

            with tqdm(total=len(tasks), desc="Processing Tasks") as progress_bar:
                while tasks_to_process:
                    future_to_task = {
                        pool.submit(task.func, *task.args, **task.kwargs): task
                        for task in tasks_to_process
                    }

                    tasks_to_retry = []

                    for future in as_completed(future_to_task):
                        task = future_to_task[future]
                        try:
                            result = future.result(timeout=task.timeout)
                            task.result = result
                            results[task.name] = result
                            logger.info(f"Task '{task.name}' completed successfully.")
                            progress_bar.update(1)

                        except TimeoutError:
                            error_msg = f"Task '{task.name}' timed out after {task.timeout} seconds."
                            logger.error(error_msg)
                            task.error = TimeoutError(error_msg)
                            results[task.name] = task.error
                            progress_bar.update(1)

                        except Exception as e:
                            if task.retries > 0:
                                task.retries -= 1
                                logger.warning(
                                    f"Task '{task.name}' failed. Retrying ({task.retries} retries left)... Error: {e}"
                                )
                                tasks_to_retry.append(task)
                            else:
                                logger.error(f"Task '{task.name}' failed after all retries: {e}")
                                task.error = e
                                results[task.name] = e
                                progress_bar.update(1)

                    tasks_to_process = tasks_to_retry

        return results
