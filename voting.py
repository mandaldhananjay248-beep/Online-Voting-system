import json

class VotingSystem:
    def __init__(self, candidates_file='data/candidates.json'):
        self.candidates_file = candidates_file
        self.load_candidates()
    
    def load_candidates(self):
        try:
            with open(self.candidates_file, 'r') as f:
                self.candidates = json.load(f)
        except FileNotFoundError:
            self.candidates = {
                "BJP": "Bharatiya Janata Party",
                "AAP": "Aam Aadmi Party", 
                "BSP": "Bahujan Samaj Party",
                "INC": "Indian National Congress",
                "NPP": "National People's Party"
            }
            self.save_candidates()
    
    def save_candidates(self):
        with open(self.candidates_file, 'w') as f:
            json.dump(self.candidates, f, indent=4)
    
    def get_candidates(self):
        return self.candidates
    
    def validate_candidate(self, candidate):
        return candidate in self.candidates