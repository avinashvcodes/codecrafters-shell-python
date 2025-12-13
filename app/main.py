import sys
import shutil
import os
import subprocess

from app.tokenizer import tokenize

BUILTIN_NAMES = {"exit", "echo", "type", "pwd"}

def cd(args):
    path = os.path.expanduser(args[0])
    if len(args) > 1:
        return None, "cd: too many arguments"

    try:
        os.chdir(path)
        return None, None
    except OSError:
        return None, f"cd: {path}: No such file or directory"


def echo(args):
    return " ".join(args), None

def get_type(cmds):
    for cmd in cmds:
        if cmd in BUILTIN_NAMES:
            return f"{cmd} is a shell builtin", None

        path = shutil.which(cmd)

        if path:
            return f"{cmd} is {path}", None

        return None, f"{cmd}: not found"

BUILTINS = {
    "exit": lambda _: sys.exit(),
    "pwd": lambda _: print(os.getcwd()),
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
            return stdout.decode().strip(), stderr.decode().strip()

    return None, f"{c}: command not found"

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
            print(stdout)
        if stderr:
            print(stderr)

def redirect(operator, cmd, file):
    to_terminal = None
    to_file = None
    stdout, stderr = execute(cmd)
    if operator in ["2>>", "1>>", ">>"]:
        mode = "a"
    else:
        mode = "w"
    if operator in ["1>", ">", "1>>", ">>"]:
        to_file = stdout
        to_terminal = stderr
    if operator in ["2>", "2>>"]:
        to_file = stderr
        to_terminal = stdout
    if to_terminal:
        print(to_terminal)
    with open(file, mode, encoding="utf-8") as f:
        if to_file:
            f.write(to_file)

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        line = sys.stdin.readline().strip()
        if not line:
            continue
        tokens = tokenize(line)
        parse(tokens)


if __name__ == "__main__":
    main()
