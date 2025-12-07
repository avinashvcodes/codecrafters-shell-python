import sys
import shutil
import os
import subprocess

BUILTIN_NAMES = {"exit", "echo", "type", "pwd"}

def cd(args):
    path = args[0]
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
    "exit": lambda *_: sys.exit(),
    "pwd": lambda *_: print(os.getcwd()),
    "cd": lambda *_: cd(),
    "echo": echo,
    "type": get_type
}

def main():

    while True:
        sys.stdout.write("$ ")
        # sys.stdout.flush()
        # when switching from write to read stdout flushes

        line = sys.stdin.readline().strip()
        if not line:
            continue
        cmd, *args = line.split(" ")

        if cmd in BUILTINS:
            BUILTINS[cmd](args)
        elif exe:= shutil.which(cmd):
            with subprocess.Popen([cmd]+args, executable=exe) as sp:
                sp.wait()
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
