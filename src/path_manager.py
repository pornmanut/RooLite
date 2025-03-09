import random
from .platform import Platform

class Path:
    def __init__(self, base_x, variation, difficulty=1.0):
        self.base_x = base_x
        self.variation = variation
        self.is_viable = True
        self.difficulty = difficulty
        self.fade_time = 2.0

    def get_next_x(self, window_width):
        """Get next x position within path's range"""
        min_x = max(0, self.base_x - self.variation)
        max_x = min(window_width - Platform.MAX_WIDTH, self.base_x + self.variation)
        
        if min_x > max_x:
            return window_width // 2
            
        return random.randint(int(min_x), int(max_x))

class PathManager:
    def __init__(self, window_width, platform_spacing):
        self.window_width = window_width
        self.platform_spacing = platform_spacing
        self.paths = []
        self.min_path_distance = 200
        self.difficulty = 1.0

    def initialize_path(self):
        """Create initial center path"""
        center_path = Path(self.window_width // 2, 100)
        self.paths = [center_path]

    def update_difficulty(self, height):
        """Update difficulty based on height"""
        self.difficulty = min(2.0, 1.0 + (abs(height) / 2000))

    def should_split(self):
        """Determine if paths should split"""
        return len(self.paths) == 1 and random.random() < 0.2 * self.difficulty

    def split_paths(self):
        """Split into two parallel paths"""
        if len(self.paths) != 1:
            return

        # Create two paths with proper spacing
        left_x = self.window_width // 4
        right_x = (self.window_width * 3) // 4
        
        self.paths = [
            Path(left_x, 50, self.difficulty),
            Path(right_x, 50, self.difficulty)
        ]

    def get_platform_positions(self, height):
        """Get platform positions for current paths"""
        positions = []
        
        # Update difficulty
        self.update_difficulty(height)
        
        # Handle path splitting with height-based chance
        if height < -500 and self.should_split():  # Only split after some height
            self.split_paths()
        
        # Generate platform positions for each path
        for path in self.paths:
            if path.is_viable:
                x = path.get_next_x(self.window_width)
                positions.append({
                    'x': x,
                    'y': height,
                    'difficulty': self.difficulty,
                    'fade_time': path.fade_time
                })

        return positions

    def cleanup(self, min_height):
        """Reset to single path if needed"""
        if len(self.paths) > 1 and random.random() < 0.1:
            self.paths = [Path(self.window_width // 2, 150, self.difficulty)]
