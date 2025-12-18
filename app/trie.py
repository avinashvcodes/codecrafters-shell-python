class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def get_prefix_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def all_words_with_prefix(self, prefix):
        words = []
        node = self.get_prefix_node(prefix)
        if not node:
            return words

        self._get_word(node, prefix, words)

        return words

    def _get_word(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            self._get_word(child_node, prefix + char, words)

    def lcp(self, prefix):

        node = self.get_prefix_node(prefix)
        if not node:
            return prefix
        while len(node.children)==1:
            char = next(iter(node.children))
            prefix += char
            node = node.children[char]

        return prefix
