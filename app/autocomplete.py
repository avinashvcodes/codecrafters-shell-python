import readline
import sys
from app.shell import Shell
from dataclasses import dataclass

@dataclass
class CompletionState:
    last_text: str = ""
    tab_count: int = 0

shell = Shell()

## Custom completer that simulates overridden readline behavior by suppressing
## readline’s internal completion logic and managing TAB state manually

def completer(text, state):
    full_line = readline.get_line_buffer()
    if state > 0:
        return None
    if CompletionState.last_text != text:
        CompletionState.last_text = text
        CompletionState.tab_count = 0
    trie = shell.get_trie()
    matches = trie.all_words_with_prefix(text)
    if CompletionState.tab_count == 0 and state == 0:
        CompletionState.tab_count += 1
        if len(matches) == 1:
            CompletionState.tab_count = 0
            return matches[0] + " "
        sys.stdout.write("\a")
        sys.stdout.flush()
        return trie.lcp(text)
    if CompletionState.tab_count == 1 and state == 0:
        CompletionState.tab_count = 0
        if matches:
            display_matches(matches, full_line)

    return None


def display_matches(matches, full_line):
    sys.stdout.write("\n" + "  ".join(sorted(matches)) + "\n")
    sys.stdout.write("$ " + full_line)
    sys.stdout.flush()

def setup_autocomplete():
    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")

# if len(matches) > 100:
#             sys.stdout.write(f"Display all {len(matches)} possibilities? (y or n)")
#             while True:
#                 c = sys.stdin.read(1)
#                 if c in {"y", "n"}:
#                     break
#                 sys.stdout.write("\a")
#                 sys.stdout.flush()
#             if c == "y":
#                 display_matches(matches, text)
#             else:
#                 sys.stdout.write("$ " + text)
#                 sys.stdout.flush()
#         else:
#             display_matches(matches, text)