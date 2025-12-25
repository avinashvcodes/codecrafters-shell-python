import os
import readline
from app.constants import BUILTIN_NAMES
from app.trie import Trie

history_file_path = os.path.expanduser("~/.pyshell_history")

if os.path.exists(history_file_path):
    readline.read_history_file(history_file_path)

readline.set_auto_history(True)

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

    def flush_history(self):
        readline.write_history_file(history_file_path)

    def get_history(self, n=0, width=5):
        length = readline.get_current_history_length()
        start = max(length-n+1, 1) if n > 0 else 1

        lines = []
        for i in range(start, length + 1):
            cmd = readline.get_history_item(i)
            if cmd:
                lines.append(f"{i:>{width}}  {cmd}")

        return "\n".join(lines) + "\n"
