from typing import Callable, List, Dict, Any, Tuple


class Task:

    def __init__(
        self,
        depends_on: List[str] = None,
        name: str = None,
        func: Callable =None,
        args: Tuple = (),
        kwargs: Dict = None,
        retries: int = 0,
        timeout: int = None
    ):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.retries = retries
        self.timeout = timeout
        self.result: Any = None
        self.error: Exception = None
        if depends_on is None:
            self.depends_on = []
        elif isinstance(depends_on, str):
            self.depends_on = [depends_on]
        elif isinstance(depends_on, list):
            self.depends_on = [item for sub in depends_on for item in (sub if isinstance(sub, list) else [sub])]
        else:
            raise TypeError("depends_on must be a string or list of strings")
