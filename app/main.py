import sys
import os

BUILTIN_NAMES = {"exit", "echo", "type"}

def next_line():
    sys.stdout.write("\n")
    sys.stdout.flush()

def echo(args):
    sys.stdout.write(" ".join(args))
    next_line()

def get_folder_paths():
    return os.getenv("PATH").split(";")

def get_file_paths(folder_path):
    file_paths = []
    for f in os.listdir(folder_path):
        full_path = os.path.join(folder_path, f)
        if os.path.isfile(full_path):
            file_paths.append((f, full_path))
    return file_paths

def check_command(cmd):
    folder_paths = get_folder_paths()
    for folder_path in folder_paths:
        file_paths = get_file_paths(folder_path)

        for file_path in file_paths:
            if cmd == file_path[0].split(".")[0] and os.access(file_path[1], os.X_OK):
                return True, file_path

    return False, ""

def get_type(cmds):
    for cmd in cmds:
        if cmd in BUILTIN_NAMES:
            sys.stdout.write(f"{cmd} is a shell builtin")
        else:
            present, message = check_command(cmd)

            if present:
                sys.stdout.write(f"{cmd} is {message}")
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
