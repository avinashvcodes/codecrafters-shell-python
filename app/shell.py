import os
from app.constants import BUILTIN_NAMES
from app.trie import Trie
class Shell:

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Shell, cls).__new__(cls)

    def __init__(self):
        self._exec_cache = None
        self.trie = None
        self.history = []

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
