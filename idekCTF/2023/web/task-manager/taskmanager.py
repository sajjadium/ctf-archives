import pydash

class TaskManager:
    protected = ["set", "get", "get_all", "__init__", "complete"]

    def __init__(self):
        self.set("capture the flag", "incomplete")

    def set(self, task, status):
        if task in self.protected:
            return
        pydash.set_(self, task, status)
        return True

    def complete(self, task):
        if task in self.protected:
            return
        pydash.set_(self, task, False)
        return True

    def get(self, task):
        if hasattr(self, task):
            return {task: getattr(self, task)}
        return {}

    def get_all(self):
        return self.__dict__