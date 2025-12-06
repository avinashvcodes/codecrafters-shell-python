import sys
import shutil
import subprocess

BUILTIN_NAMES = {"exit", "echo", "type"}

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
            with subprocess.Popen([exe]+args) as sp:
                sp.wait()
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
