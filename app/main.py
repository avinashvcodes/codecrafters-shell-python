import sys
import shutil
import os
import subprocess

from app.tokenizer import tokenize

BUILTIN_NAMES = {"exit", "echo", "type", "pwd"}

def cd(args):
    path = os.path.expanduser(args[0])
    if len(args) > 1:
        print("cd: too many arguments")
        return

    try:
        os.chdir(path)
    except OSError:
        print(f"cd: {path}: No such file or directory")


def echo(args):
    print(" ".join(args))

def get_type(cmds):
    for cmd in cmds:
        if cmd in BUILTIN_NAMES:
            print(f"{cmd} is a shell builtin")
        else:
            path = shutil.which(cmd)

            if path:
                print(f"{cmd} is {path}")
            else:
                print(f"{cmd}: not found")

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
        BUILTINS[c](args)
        return None, None
    if exe:= shutil.which(c):
        with subprocess.Popen([c]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable=exe) as sp:
            stdout, stderr = sp.communicate()
            return stdout, stderr

    print(f"{c}: command not found")
    return None, None

def parse(tokens: list[str]):

    l, r = 0, len(tokens)
    cmd = []
    while l<r:
        token = tokens[l]
        if token in {"1>", ">"}:
            stdout, stderr = execute(cmd)
            if stderr:
                print(str(stderr))
            l+=1
            file = tokens[l]
            with open(file, "w", encoding="utf-8") as f:
                f.write(str(stdout))
            l+=1
            cmd = []
            continue
        cmd.append(tokens[l])
        l+=1

    if cmd:
        stdout, stderr = execute(cmd)
        if stdout:
            print(str(stdout))
        if stderr:
            print(str(stderr))



def main():

    while True:
        sys.stdout.write("$ ")
        # sys.stdout.flush()
        # when switching from write to read stdout flushes automatically

        line = sys.stdin.readline().strip()
        if not line:
            continue
        tokens = tokenize(line)
        parse(tokens)


if __name__ == "__main__":
    main()
