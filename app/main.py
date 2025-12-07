import sys
import shutil
import util
import os
import subprocess

BUILTIN_NAMES = {"exit", "echo", "type", "pwd"}

def tokenize(s: str):

    l, r = 0, len(s)
    tokens = []
    while l<r:

        while l<r and s[l].isspace():
            l+=1

        if l==r:
            break

        in_single_quote = False
        in_double_quote = False

        word = ""
        while l<r:
            if not in_single_quote and not in_double_quote and s[l].isspace():
                break

            if s[l] == "'" and not in_double_quote:
                in_single_quote = not in_single_quote

            elif s[l] == '"' and not in_single_quote:
                in_double_quote = not in_double_quote

            else:
                word+=s[l]

            l+=1

        if word:
            tokens.append(word)

    return tokens


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

def main():

    while True:
        sys.stdout.write("$ ")
        # sys.stdout.flush()
        # when switching from write to read stdout flushes

        line = sys.stdin.readline().strip()
        if not line:
            continue
        cmd, *args = util.tokenize(line)

        if cmd in BUILTINS:
            BUILTINS[cmd](args)
        elif exe:= shutil.which(cmd):
            with subprocess.Popen([cmd]+args, executable=exe) as sp:
                sp.wait()
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()
