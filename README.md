# FlowForge  

**FlowForge** is a lightweight Python workflow orchestration tool inspired by Apache Airflow.  
It lets you define **DAGs** (Directed Acyclic Graphs), manage **dependencies**, and execute tasks concurrently with retries, timeouts, and logging. 

---

## ✨ Features  

- 🕸️ Define tasks and dependencies with ease  
- ⏱️ Task retries and timeout handling  
- ⚡ Concurrent execution via `ThreadPoolExecutor`  
- 📊 Progress bar with `tqdm`  
- 📝 Structured logging for task success/failure  
- 🔗 Lightweight, no heavy external dependencies  

---

## 📦 Installation  

Clone the repo:  

```bash
git clone https://github.com/bilgesubukk/flowforge.git
````

---

## 🚀 Quickstart Example

```python
from time import sleep
from src.flowforge import DAG, Task, Executor, Scheduler

# Define sample tasks
def task_a():
    sleep(1)
    return "Task A done"

def task_b():
    sleep(2)
    return "Task B done"

def task_c():
    sleep(1)
    return "Task C done"

# Build DAG
dag = DAG(name="example_dag")
dag.add_task(Task(name="A", func=task_a))
dag.add_task(Task(name="B", func=task_b, depends_on=["A"]))
dag.add_task(Task(name="C", func=task_c, depends_on=["B"]))

# Run DAG
executor = Executor(max_workers=2)
scheduler = Scheduler(dag=dag, executor=executor)
scheduler.run()
```

✅ **Output example**

```
Processing Tasks: 100%|██████████| 3/3 [00:04<00:00, ...]
Task 'A' completed successfully.
Task 'B' completed successfully.
Task 'C' completed successfully.
```

---

## 🧪 Running Tests

Install dev dependencies:

```bash
pip install -r requirements.txt
```

Run tests with `pytest`:

```bash
pytest -v
```

---

## 📌 Roadmap

* [ ] Add cron-style scheduling
* [ ] Add persistence

---
