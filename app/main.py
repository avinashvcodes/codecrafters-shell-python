import sys
import shutil
import os
import subprocess
import readline

from app.tokenizer import tokenize

BUILTIN_NAMES = {"exit", "echo", "type", "pwd"}

class Shell:
    def __init__(self):
        self._exec_cache = None

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

def cd(args):
    path = os.path.expanduser(args[0])
    if len(args) > 1:
        return None, "cd: too many arguments\n"

    try:
        os.chdir(path)
        return None, None
    except OSError:
        return None, f"cd: {path}: No such file or directory\n"


def echo(args):
    return " ".join(args)+"\n", None

def get_type(cmds):
    for cmd in cmds:
        if cmd in BUILTIN_NAMES:
            return f"{cmd} is a shell builtin\n", None

        path = shutil.which(cmd)

        if path:
            return f"{cmd} is {path}\n", None

        return None, f"{cmd}: not found\n"

def pwd(args):
    return os.getcwd() + "\n", None

BUILTINS = {
    "exit": lambda _: sys.exit(),
    "pwd": pwd,
    "cd": cd,
    "echo": echo,
    "type": get_type
}

def execute(cmd: list):

    c, *args = cmd
    if c in BUILTINS:
        output = BUILTINS[c](args)
        if output:
            stdout, stderr = output
            return stdout, stderr
        return None, None
    if exe:= shutil.which(c):
        with subprocess.Popen([c]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable=exe) as sp:
            stdout, stderr = sp.communicate()
            return stdout.decode(), stderr.decode()

    return None, f"{c}: command not found\n"

def parse(tokens: list[str]):

    l, r = 0, len(tokens)
    cmd = []
    while l<r:
        token = tokens[l]
        if token in {"1>", ">", "2>", ">>", "1>>", "2>>"}:
            redirect(token, cmd, tokens[l+1])
            l+=2
            cmd = []
        if l < r:
            cmd.append(tokens[l])
        l+=1

    if cmd:
        stdout, stderr = execute(cmd)
        if stdout:
            sys.stdout.write(stdout)
        if stderr:
            sys.stderr.write(stderr)

def redirect(operator, cmd, file):
    to_terminal = None
    to_file = None
    terminal_stream = None
    stdout, stderr = execute(cmd)
    if operator in ["2>>", "1>>", ">>"]:
        mode = "a"
    else:
        mode = "w"
    if operator in ["1>", ">", "1>>", ">>"]:
        to_file = stdout
        to_terminal = stderr
        terminal_stream = sys.stderr
    if operator in ["2>", "2>>"]:
        to_file = stderr
        to_terminal = stdout
        terminal_stream = sys.stdout
    if to_terminal:
        terminal_stream.write(to_terminal)
    with open(file, mode, encoding="utf-8") as f:
        if to_file:
            f.write(to_file)

shell = Shell()
def completer(text, state):
    options = [cmd for cmd in shell.get_executables() if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

def display_matches(substitution, matches, longest_match_length):
    sys.stdout.write("\n" + "  ".join(matches) + "\n")
    sys.stdout.write("$ " + readline.get_line_buffer())
    sys.stdout.flush()

readline.set_completer(completer)
readline.set_completion_display_matches_hook(display_matches)
readline.parse_and_bind("tab: complete")

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        line = input().strip()
        if not line:
            continue
        tokens = tokenize(line)
        parse(tokens)


if __name__ == "__main__":
    main()
