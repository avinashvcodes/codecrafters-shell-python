import sys


def main():

    while True:
        sys.stdout.write("$ ")
        # sys.stdout.flush()
        # when switching from write to read stdout flushes

        command = sys.stdin.readline().strip()
        sys.stdout.write(f"{command}: command not found")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
