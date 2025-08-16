class Storage:
    """Simple storage to track task results in memory."""
    def __init__(self):
        self.data = {}

    def set(self, task_name, value):
        self.data[task_name] = value

    def get(self, task_name):
        return self.data.get(task_name)
