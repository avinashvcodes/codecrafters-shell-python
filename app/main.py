import sys

BUILTIN_NAMES = {"exit", "echo", "type"}

def next_line():
    sys.stdout.write("\n")
    sys.stdout.flush()

def echo(args):
    sys.stdout.write(" ".join(args))
    next_line()

def get_type(cmds):
    for cmd in cmds:
        if cmd in BUILTIN_NAMES:
            sys.stdout.write(f"{cmd} is a shell builtin")
            next_line()
        else:
            sys.stdout.write(f"{cmd}: not found")
            next_line()


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

        try:
            BUILTINS[cmd](args)
        except KeyError:
            sys.stdout.write(f"{cmd}: command not found")
            next_line()

if __name__ == "__main__":
    main()
