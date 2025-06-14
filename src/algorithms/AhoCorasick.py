from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.pattern_index = -1 #inisialisasi 
        self.failure_link = None
        self.output_link = None

class AhoCorasick:
    def __init__(self, patterns: str):
        self.patterns = [pattern.strip().lower() for pattern in patterns.split(',') if pattern.strip()]
        self.root = TrieNode()
        self.build_trie()
        self.build_failure_links()
        self.build_output_links()

    def get_patterns(self):
        return self.patterns
    
    def build_trie(self):
        for pattern_idx, pattern in enumerate(self.patterns):
            current_node = self.root
            for char in pattern:
                if char not in current_node.children:
                    current_node.children[char] = TrieNode()
                current_node = current_node.children[char]
            current_node.is_end_of_word = True
            current_node.pattern_index = pattern_idx
    
    def build_failure_links(self):        
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
                
                while failure_node is not None and char not in failure_node.children:
                    failure_node = failure_node.failure_link
                
                if failure_node is not None:
                    child_node.failure_link = failure_node.children[char]
                else:
                    child_node.failure_link = self.root
    
    def build_output_links(self):
        queue = deque([self.root])
        
        while queue:
            current_node = queue.popleft()
            
            for child_node in current_node.children.values():
                queue.append(child_node)
                
                failure_node = child_node.failure_link
                
                if failure_node.is_end_of_word:
                    child_node.output_link = failure_node
                else:
                    child_node.output_link = failure_node.output_link
    
    def search(self, text: str):
        text = text.lower()
        found_matches = []
        current_node = self.root
        
        for i, char in enumerate(text):
            while current_node is not None and char not in current_node.children:
                current_node = current_node.failure_link
            
            if current_node is None:
                current_node = self.root
                continue
            
            current_node = current_node.children[char]
            
            temp_node = current_node
            while temp_node is not None:
                if temp_node.is_end_of_word:
                    pattern = self.patterns[temp_node.pattern_index]
                    start_pos = i - len(pattern) + 1
                    found_matches.append({
                        'pattern': pattern,
                        'position': start_pos,
                        'pattern_index': temp_node.pattern_index
                    })
                temp_node = temp_node.output_link
        
        grouped_matches = {}
        for i, pattern in enumerate(self.patterns):
            grouped_matches[pattern] = {
                'pattern_index': i,
                'positions': []
            }
        
        for match in found_matches:
            pattern = match['pattern']
            grouped_matches[pattern]['positions'].append(match['position'])

        return grouped_matches
    
# if __name__ == "__main__":
#     ac = AhoCorasick("IN, con, Fro, it, que, c, is")
#     text = "conquER From WithInis in in in"
    
#     grouped = ac.search(text)
#     for pattern, data in grouped.items():
#         print(f"Pattern '{pattern}': {data['positions']}")