from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.pattern_index = -1 #inisialisasi 
        self.failure_link = None
        self.output_link = None

class AhoCorasick:
    def __init__(self, patterns_str: str):
        self.patterns = []
        self.root = TrieNode()
        self.set_pattern(patterns_str)

    def set_pattern(self, patterns_str: str):
        self.patterns = [pattern.strip().lower() for pattern in patterns_str.split(',') if pattern.strip()]
        self.root = TrieNode()
        self._build_trie()
        self._build_failure_and_output_links()

    def get_patterns(self):
        return self.patterns
    
    def _build_trie(self):
        for pattern_idx, pattern in enumerate(self.patterns):
            current_node = self.root
            for char in pattern:
                current_node = current_node.children.setdefault(char, TrieNode())
            current_node.is_end_of_word = True
            current_node.pattern_index = pattern_idx
    
    def _build_failure_and_output_links(self):
        self.root.failure_link = self.root
        queue = deque()
        
        # failure link semua node di level 1 adalah root
        for child in self.root.children.values():
            child.failure_link = self.root
            queue.append(child)
        
        while queue:
            current_node = queue.popleft()
            
            for char, child_node in current_node.children.items():
                queue.append(child_node)
                
                failure_node = current_node.failure_link
                while char not in failure_node.children and failure_node is not self.root:
                    failure_node = failure_node.failure_link
                
                if char in failure_node.children:
                    child_node.failure_link = failure_node.children[char]
                else:
                    child_node.failure_link = self.root
                if child_node.failure_link.is_end_of_word:
                    child_node.output_link = child_node.failure_link
                else:
                    child_node.output_link = child_node.failure_link.output_link
    
    def search(self, text: str):
        text = text.lower()
        results = {pattern: 0 for pattern in self.patterns}
        current_node = self.root
        
        for i, char in enumerate(text):
            while char not in current_node.children and current_node is not self.root:
                current_node = current_node.failure_link
            
            if char in current_node.children:
                current_node = current_node.children[char]
            else:
                continue
            
            temp_node = current_node
            while temp_node is not None:
                if temp_node.is_end_of_word:
                    pattern = self.patterns[temp_node.pattern_index]
                    
                    results[pattern] += 1
                
                temp_node = temp_node.output_link
        
        return results