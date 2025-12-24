import os
from app.constants import BUILTIN_NAMES
from app.trie import Trie

history_file_path = os.path.expanduser("~/.pyshell_history")

class Shell:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if getattr(self, "_declared", False):
            return
        self._declared = True

        self._exec_cache = None
        self.trie = None
        self.history = self.load_history()
        self._history_start_index = len(self.history)

    def load_history(self):
        history = []
        if os.path.exists(history_file_path):
            with open(history_file_path, "r", encoding='utf-8') as f:
                for line in f:
                    history.append(line.strip("\n"))
        return history

    def get_executables(self):
        if self._exec_cache is not None:
            return self._exec_cache

        executables = set(BUILTIN_NAMES)
        for directory in os.getenv("PATH", "").split(os.pathsep):
            if os.path.isdir(directory):
                for file in os.listdir(directory):
                    full_path = os.path.join(directory, file)
                    if os.access(full_path, os.X_OK) and os.path.isfile(full_path):
                        executables.add(file)

        self._exec_cache = executables
        return executables

    def get_trie(self):
        if self.trie is None:
            self.trie = Trie()
            for cmd in self.get_executables():
                self.trie.insert(cmd)
        return self.trie

    def add_history(self, command: str):
        self.history.append(command)

    def flush_history(self):
        if not self.history:
            return
        with open(history_file_path, "a", encoding='utf-8') as f:
            for command in self.history[self._history_start_index:]:
                f.write(command + "\n")
        self.history.clear()

    def get_history(self, width=5):
        lines = []
        for i, command in enumerate(self.history, start=1):
            lines.append(f"{i:>{width}}  {command}")
        return "\n".join(lines) + "\n"
