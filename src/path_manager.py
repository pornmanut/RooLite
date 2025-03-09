import random
from .platform import Platform

class Path:
    def __init__(self, base_x, variation, difficulty=1.0):
        self.base_x = base_x
        self.variation = variation
        self.is_viable = True
        self.difficulty = difficulty
        self.fade_time = 2.0
        self.split_duration = 0
        self.merge_threshold = random.randint(800, 1200)

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
        self.split_start_height = 0
        self.current_height = 0
        self.moving_platform_chance = 0.0

    def initialize_path(self):
        """Create initial center path"""
        center_path = Path(self.window_width // 2, 100)
        self.paths = [center_path]
        self.current_height = 0
        self.moving_platform_chance = 0.0

    def update_difficulty(self, height):
        """Update difficulty based on height"""
        self.difficulty = min(2.0, 1.0 + (abs(height) / 2000))
        self.current_height = abs(height)
        
        # Reduced spawn rate: Start at 250 height, reach max (0.2) at 2000 height
        if self.current_height > 250:
            self.moving_platform_chance = min(0.2, (self.current_height - 250) / 4000)

    def should_split(self):
        """Determine if paths should split"""
        if len(self.paths) != 1:
            return False
            
        if self.current_height < 500:
            return False
            
        base_chance = 0.2 * self.difficulty
        return random.random() < base_chance

    def should_merge(self):
        """Determine if parallel paths should merge"""
        if len(self.paths) <= 1:
            return False
            
        height_traveled = self.current_height - self.split_start_height
        return height_traveled > self.paths[0].merge_threshold

    def get_moving_platform_type(self):
        """Determine if and what type of moving platform to create"""
        if self.current_height <= 250:
            return None
            
        if random.random() >= self.moving_platform_chance:
            return None
            
        # Random speed category for variety
        return random.choice(['moving_slow', 'moving_medium', 'moving_fast'])

    def merge_paths(self):
        """Merge paths back to center"""
        if len(self.paths) <= 1:
            return
            
        center_path = Path(self.window_width // 2, 150, self.difficulty)
        
        for path in self.paths:
            path.is_viable = False
            path.fade_time = 1.0
            
        self.paths = [center_path]

    def split_paths(self):
        """Split into two parallel paths"""
        if len(self.paths) != 1:
            return

        self.split_start_height = self.current_height
        
        left_x = self.window_width // 4
        right_x = (self.window_width * 3) // 4
        
        self.paths = [
            Path(left_x, 50, self.difficulty),
            Path(right_x, 50, self.difficulty)
        ]

    def get_platform_positions(self, height):
        """Get platform positions for current paths"""
        positions = []
        
        self.update_difficulty(height)
        
        if self.should_merge():
            self.merge_paths()
        elif self.should_split():
            self.split_paths()
        
        for path in self.paths:
            if path.is_viable:
                x = path.get_next_x(self.window_width)
                platform_type = self.get_moving_platform_type() or 'normal'
                
                positions.append({
                    'x': x,
                    'y': height,
                    'difficulty': self.difficulty,
                    'fade_time': path.fade_time,
                    'platform_type': platform_type
                })

        return positions

    def cleanup(self, min_height):
        """Clean up old paths"""
        self.paths = [p for p in self.paths if p.is_viable]
        
        if not self.paths:
            self.paths = [Path(self.window_width // 2, 150, self.difficulty)]
