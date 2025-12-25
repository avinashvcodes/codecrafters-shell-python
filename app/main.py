import sys
import shutil
import os
import subprocess
import signal
import readline

from app.autocomplete import setup_autocomplete
from app.constants import BUILTIN_NAMES
from app.tokenizer import tokenize
from app.shell import Shell, Pointer

HISTFILE = os.environ.get("HISTFILE")
history_file_path = os.path.expanduser(HISTFILE)
shell = Shell()

def on_signal(signum, frame):
    shell.flush_history()
    sys.exit(0)
signal.signal(signal.SIGTERM, on_signal)
signal.signal(signal.SIGINT, on_signal)

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

def get_history(args):
    try:
        if args and args[0].startswith('-'):
            file = args[1] if len(args) > 1 else history_file_path
            if args[0] == '-r':
                if file != history_file_path:
                    readline.read_history_file(file)
                return None, None
            if args[0] == '-w':
                readline.write_history_file(file)
                Pointer.already_written = readline.get_current_history_length()
                return None, None
            if args[0] == '-a':
                readline.append_history_file(readline.get_current_history_length() - Pointer.already_written, file)
                Pointer.already_written = readline.get_current_history_length()
                return None, None
        n = int(args[0]) if args else 0
    except ValueError:
        return None, f"history: {args[0]}: numeric argument required\n"
    return shell.get_history(n), None

BUILTINS = {
    "exit": lambda _: sys.exit(),
    "pwd": pwd,
    "cd": cd,
    "echo": echo,
    "type": get_type,
    "history": get_history
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

def execute_buildins(cmd: list):
    c, *args = cmd
    if c in BUILTINS:
        output = BUILTINS[c](args)
        if output:
            stdout, stderr = output
            if stderr:
                sys.stderr.write(stderr)
            if stdout:
                sys.stdout.write(stdout)
    else:
        sys.stderr.write(f"{c}: command not found\n")

def parse(tokens: list[str]):

    l, r = 0, len(tokens)
    cmd = []
    while l<r:
        token = tokens[l]
        if token in {"1>", ">", "2>", ">>", "1>>", "2>>"}:
            redirect(token, cmd, tokens[l+1])
            l+=2
            cmd = []
        if token == "|":
            cmds = [cmd]
            while l < r and tokens[l] == "|":
                l+=1
                cmd2 = []
                while l < r and tokens[l] not in {"|", "1>", ">", "2>", ">>", "1>>", "2>>"}:
                    cmd2.append(tokens[l])
                    l+=1
                cmds.append(cmd2)
            pipe(cmds)
            cmd = []
            continue
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

def pipe(cmds):
    processes = []
    prev_r = None
    for i in range(len(cmds)-1):
        cmd = cmds[i]
        r, w = os.pipe()
        if cmd[0] in BUILTIN_NAMES:
            stdin_ = os.dup(0)
            stdout_ = os.dup(1)
            if prev_r is not None:
                os.dup2(prev_r, 0)
                os.close(prev_r)
            os.dup2(w, 1)
            os.close(w)
            execute_buildins(cmd)
            os.dup2(stdin_, 0)
            os.dup2(stdout_, 1)
            os.close(stdin_)
            os.close(stdout_)
            prev_r = r
            continue

        pid = os.fork()
        processes.append(pid)
        if pid == 0:
            os.dup2(w, 1)
            if prev_r is not None:
                os.dup2(prev_r, 0)
                os.close(prev_r)
            os.close(r)
            os.close(w)
            os.execvp(cmd[0], cmd)
        os.close(w)
        if prev_r is not None:
            os.close(prev_r)
        prev_r = r

    cmd = cmds[-1]
    if cmd[0] in BUILTIN_NAMES:
        stdin_ = os.dup(0)
        if prev_r is not None:
            os.dup2(prev_r, 0)
            os.close(prev_r)
        execute_buildins(cmd)
        os.dup2(stdin_, 0)
        os.close(stdin_)
        return  # Exit cause the last is a built-in command
    pid = os.fork()
    processes.append(pid)
    if pid == 0:
        if prev_r is not None:
            os.dup2(prev_r, 0)
            os.close(prev_r)
        os.execvp(cmd[0], cmd)

    if prev_r is not None:
        os.close(prev_r)

    for pid in processes:
        os.waitpid(pid, 0)

def main():
    setup_autocomplete()
    try:
        while True:
            line = input("$ ").strip()
            if not line:
                continue
            readline.add_history(line)
            tokens = tokenize(line)
            parse(tokens)
    finally:
        shell.flush_history()

if __name__ == "__main__":
    main()
