import sys


def main():

    while True:
        sys.stdout.write("$ ")
        # sys.stdout.flush()
        # when switching from write to read stdout flushes

        command = sys.stdin.readline().strip()
        if command == "exit":
            break
        if command.startswith("echo "):
            sys.stdout.write(f"{command[5:]}\n")
            sys.stdout.flush()
        else:
            sys.stdout.write(f"{command}: command not found\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
