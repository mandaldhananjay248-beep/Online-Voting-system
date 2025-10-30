import heapq
import json

class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, candidate, votes):
        # Using negative votes for max heap behavior
        heapq.heappush(self.heap, (-votes, candidate))
    
    def pop(self):
        if self.heap:
            votes, candidate = heapq.heappop(self.heap)
            return candidate, -votes
        return None
    
    def get_top_k(self, k=5):
        # Create a copy to avoid modifying original
        temp_heap = self.heap.copy()
        results = []
        
        for _ in range(min(k, len(temp_heap))):
            votes, candidate = heapq.heappop(temp_heap)
            results.append((candidate, -votes))
        
        return results
    
    def build_heap(self, candidate_votes):
        self.heap = []
        for candidate, votes in candidate_votes.items():
            self.push(candidate, votes)

class Leaderboard:
    def __init__(self, votes_file='data/votes.json'):
        self.votes_file = votes_file
        self.max_heap = MaxHeap()
        self.load_votes()
    
    def load_votes(self):
        try:
            with open(self.votes_file, 'r') as f:
                self.votes = json.load(f)
        except FileNotFoundError:
            # Initialize with zero votes for all candidates
            self.votes = {"BJP": 0, "AAP": 0, "BSP": 0, "INC": 0, "NPP": 0}
            self.save_votes()
        
        self.max_heap.build_heap(self.votes)
    
    def save_votes(self):
        with open(self.votes_file, 'w') as f:
            json.dump(self.votes, f, indent=4)
    
    def add_vote(self, candidate):
        if candidate in self.votes:
            self.votes[candidate] += 1
            self.max_heap.build_heap(self.votes)
            self.save_votes()
            return True
        return False
    
    def get_leaderboard(self, top_n=5):
        return self.max_heap.get_top_k(top_n)
    
    def get_candidate_votes(self, candidate):
        return self.votes.get(candidate, 0)