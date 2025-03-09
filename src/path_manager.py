import random
from .platform import Platform

class Path:
    def __init__(self, base_x, variation, difficulty=1.0):
        self.base_x = base_x
        self.variation = variation
        self.is_viable = True
        self.difficulty = difficulty
        self.fade_time = 2.0
        self.split_duration = 0  # Track how long the path has been split
        self.merge_threshold = random.randint(800, 1200)  # Height to travel before merging

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
        self.split_start_height = 0  # Track height where split occurred
        self.current_height = 0

    def initialize_path(self):
        """Create initial center path"""
        center_path = Path(self.window_width // 2, 100)
        self.paths = [center_path]
        self.current_height = 0

    def update_difficulty(self, height):
        """Update difficulty based on height"""
        self.difficulty = min(2.0, 1.0 + (abs(height) / 2000))
        self.current_height = abs(height)

    def should_split(self):
        """Determine if paths should split"""
        if len(self.paths) != 1:
            return False
            
        # Only split after certain height and with increasing probability
        if self.current_height < 500:  # Don't split too early
            return False
            
        base_chance = 0.2 * self.difficulty
        return random.random() < base_chance

    def should_merge(self):
        """Determine if parallel paths should merge"""
        if len(self.paths) <= 1:
            return False
            
        # Check if we've traveled enough height since splitting
        height_traveled = self.current_height - self.split_start_height
        return height_traveled > self.paths[0].merge_threshold

    def merge_paths(self):
        """Merge paths back to center"""
        if len(self.paths) <= 1:
            return
            
        # Create new center path
        center_path = Path(self.window_width // 2, 150, self.difficulty)
        
        # Mark old paths as non-viable
        for path in self.paths:
            path.is_viable = False
            path.fade_time = 1.0  # Quicker fade for merging
            
        self.paths = [center_path]

    def split_paths(self):
        """Split into two parallel paths"""
        if len(self.paths) != 1:
            return

        # Remember split height
        self.split_start_height = self.current_height
        
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
        
        # Update difficulty and height tracking
        self.update_difficulty(height)
        
        # Check for path changes
        if self.should_merge():
            self.merge_paths()
        elif self.should_split():
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
        """Clean up old paths"""
        # Remove any non-viable paths
        self.paths = [p for p in self.paths if p.is_viable]
        
        # Ensure we always have at least one path
        if not self.paths:
            self.paths = [Path(self.window_width // 2, 150, self.difficulty)]
