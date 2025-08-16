from time import sleep
from src.flowforge import DAG, Task, Scheduler, Executor, get_logger

logger = get_logger("example_dag")

# ----- Define your tasks -----
def extract_data():
    logger.info("Extracting data...")
    sleep(1)  # simulate delay
    data = {"users": ["Alice", "Bob", "Charlie"]}
    logger.info(f"Data extracted: {data}")
    return data

def transform_data():
    logger.info("Transforming data...")
    sleep(1)
    transformed = {"user_count": 3}
    logger.info(f"Data transformed: {transformed}")
    return transformed

def load_data():
    logger.info("Loading data to database...")
    sleep(1)
    logger.info("Data loaded successfully!")
    return True

# ----- Build DAG -----
dag = DAG(name="example_etl")

dag.add_task(Task(name="extract", func=extract_data))
dag.add_task(Task(name="transform", func=transform_data, depends_on=["extract"]))
dag.add_task(Task(name="load", func=load_data, depends_on=["transform"]))

# ----- Run DAG -----
if __name__ == "__main__":
    executor = Executor(max_workers=2)
    scheduler = Scheduler(dag=dag, executor=executor)
    scheduler.run()
    logger.info("DAG run completed!")
