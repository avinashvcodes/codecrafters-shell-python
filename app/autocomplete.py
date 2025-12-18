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
            display_matches(matches, text)
        return text

    return None

# def get_common_prefix(text, matches):
#     if not matches:
#         return text
#     prefix = matches[0]
#     l = len(text)
#     for i in range(1, len(matches)):
#         if len(prefix) > len(matches[i]):
#             prefix = prefix[:len(matches[i])]
#         for j in range(l, len(prefix)):
#             if prefix[j] != matches[i][j]:
#                 prefix = prefix[:j]
#                 break
#         if prefix == text:
#             return text
#     return prefix

def display_matches(matches, text):
    sys.stdout.write("\n" + "  ".join(sorted(matches)) + "\n")
    sys.stdout.write("$ " + text)
    sys.stdout.flush()

def setup_autocomplete():
    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")
