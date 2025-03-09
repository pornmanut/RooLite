import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class HighScore:
    def __init__(self, player_name: str, score: int, date: Optional[str] = None):
        self.player_name = player_name[:20]  # Limit name to 20 chars
        self.score = score
        self.date = date or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "player_name": self.player_name,
            "score": self.score,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'HighScore':
        return cls(
            player_name=data["player_name"],
            score=data["score"],
            date=data["date"]
        )

class HighScoreManager:
    def __init__(self):
        self.MAX_SCORES = 10
        self.save_file_path = "data/high_scores.json"
        self.scores: List[HighScore] = []
        self._ensure_data_directory()
        self.load_scores()

    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.save_file_path), exist_ok=True)

    def load_scores(self) -> None:
        """Load high scores from file"""
        try:
            if os.path.exists(self.save_file_path):
                with open(self.save_file_path, 'r') as f:
                    data = json.load(f)
                    self.scores = [HighScore.from_dict(score_data) 
                                 for score_data in data["high_scores"]]
                    # Sort scores in descending order
                    self.scores.sort(key=lambda x: x.score, reverse=True)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            self.scores = []

    def save_scores(self) -> None:
        """Save high scores to file"""
        try:
            data = {
                "high_scores": [score.to_dict() for score in self.scores]
            }
            with open(self.save_file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def add_score(self, player_name: str, score: int) -> bool:
        """
        Add a new score and return True if it's a high score
        """
        new_score = HighScore(player_name, score)
        
        # If we have less than MAX_SCORES, it's automatically a high score
        if len(self.scores) < self.MAX_SCORES:
            self.scores.append(new_score)
            self._sort_scores()
            self.save_scores()
            return True
        
        # Check if score is higher than the lowest high score
        if score > self.scores[-1].score:
            self.scores.append(new_score)
            self._sort_scores()
            if len(self.scores) > self.MAX_SCORES:
                self.scores = self.scores[:self.MAX_SCORES]
            self.save_scores()
            return True
        
        return False

    def _sort_scores(self) -> None:
        """Sort scores in descending order"""
        self.scores.sort(key=lambda x: x.score, reverse=True)

    def get_scores(self) -> List[HighScore]:
        """Get list of high scores"""
        return self.scores

    def is_high_score(self, score: int) -> bool:
        """Check if a score qualifies as a high score"""
        if len(self.scores) < self.MAX_SCORES:
            return True
        return score > self.scores[-1].score if self.scores else True
