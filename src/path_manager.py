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
        self.base_platform_spacing = platform_spacing
        self.paths = []
        self.min_path_distance = 200
        self.difficulty = 1.0
        self.split_start_height = 0
        self.current_height = 0
        self.moving_platform_chance = 0.0
        self.platform_count_since_safe = 0
        self.last_platform_type = None
        self.in_recovery_zone = False
        self.zone_thresholds = {
            'beginner': 10000,
            'intermediate': 40000,
            'advanced': 80000
        }

    def get_current_zone(self):
        """Determine current difficulty zone based on height"""
        height = abs(self.current_height)
        if height <= self.zone_thresholds['beginner']:
            return 'beginner'
        elif height <= self.zone_thresholds['intermediate']:
            return 'intermediate'
        elif height <= self.zone_thresholds['advanced']:
            return 'advanced'
        return 'expert'

    def get_zone_parameters(self):
        """Get platform parameters based on current zone"""
        zone = self.get_current_zone()
        height = abs(self.current_height)

        params = {
            'beginner': {
                'spacing_multiplier': 0.8,
                'width_range': (0.9, 1.0),
                'split_enabled': height > 5000,
                'moving_chance_max': 0.1
            },
            'intermediate': {
                'spacing_multiplier': 0.85 + (height - self.zone_thresholds['beginner']) / 200000,
                'width_range': (0.8, 0.9),
                'split_enabled': True,
                'moving_chance_max': 0.25
            },
            'advanced': {
                'spacing_multiplier': 0.9 + (height - self.zone_thresholds['intermediate']) / 400000,
                'width_range': (0.7, 0.85),
                'split_enabled': True,
                'moving_chance_max': 0.4
            },
            'expert': {
                'spacing_multiplier': 0.95 + (height - self.zone_thresholds['advanced']) / 400000,
                'width_range': (0.6, 0.8),
                'split_enabled': True,
                'moving_chance_max': 0.5
            }
        }

        # Cap spacing multiplier to prevent impossible jumps
        params[zone]['spacing_multiplier'] = min(1.0, params[zone]['spacing_multiplier'])
        
        return params[zone]

    def initialize_path(self):
        """Create initial center path"""
        center_path = Path(self.window_width // 2, 100)
        self.paths = [center_path]
        self.current_height = 0
        self.moving_platform_chance = 0.0
        self.platform_count_since_safe = 0

    def update_difficulty(self, height):
        """Update difficulty based on height"""
        self.current_height = abs(height)

        # Calculate difficulty based on zones
        if self.current_height <= self.zone_thresholds['beginner']:
            self.difficulty = 1.0 + (self.current_height / self.zone_thresholds['beginner']) * 0.5
        elif self.current_height <= self.zone_thresholds['intermediate']:
            self.difficulty = 1.5 + ((self.current_height - self.zone_thresholds['beginner']) /
                                   (self.zone_thresholds['intermediate'] - self.zone_thresholds['beginner'])) * 0.5
        elif self.current_height <= self.zone_thresholds['advanced']:
            self.difficulty = 2.0 + ((self.current_height - self.zone_thresholds['intermediate']) /
                                   (self.zone_thresholds['advanced'] - self.zone_thresholds['intermediate'])) * 0.5
        else:
            self.difficulty = min(3.0, 2.5 + ((self.current_height - self.zone_thresholds['advanced']) /
                                            self.zone_thresholds['advanced']) * 0.5)
        
        # Update platform spacing based on zone
        zone_params = self.get_zone_parameters()
        self.platform_spacing = self.base_platform_spacing * zone_params['spacing_multiplier']
        
        # Update moving platform chance
        if self.current_height > self.zone_thresholds['beginner'] / 20:  # Start at 5% of beginner zone
            zone_params = self.get_zone_parameters()
            height_in_zone = self.current_height - (self.zone_thresholds['beginner'] / 20)
            self.moving_platform_chance = min(
                zone_params['moving_chance_max'],
                height_in_zone / (self.zone_thresholds['beginner'] * 2)
            )

    def should_split(self):
        """Determine if paths should split"""
        if len(self.paths) != 1:
            return False
            
        zone_params = self.get_zone_parameters()
        if not zone_params['split_enabled']:
            return False
            
        base_chance = 0.2 * self.difficulty
        return random.random() < base_chance

    def get_platform_type(self):
        """Determine platform type with distribution"""
        # Check for moving platform first
        moving_type = self.get_moving_platform_type()
        if moving_type:
            return moving_type

        # Force safe platform every 5 platforms
        self.platform_count_since_safe += 1
        if self.platform_count_since_safe >= 5:
            self.platform_count_since_safe = 0
            self.last_platform_type = 'normal'
            return 'normal'

        # Get current zone parameters
        zone_params = self.get_zone_parameters()
        
        # Small platform chance increases with difficulty
        small_platform_chance = 0.3 + (self.difficulty - 1.0) * 0.2
        if random.random() < small_platform_chance:
            self.last_platform_type = 'small'
            return 'small'

        # Default to normal platform
        self.last_platform_type = 'normal'
        return 'normal'

    def should_merge(self):
        """Determine if parallel paths should merge"""
        if len(self.paths) <= 1:
            return False
            
        height_traveled = self.current_height - self.split_start_height
        return height_traveled > self.paths[0].merge_threshold

    def get_moving_platform_type(self):
        """Determine if and what type of moving platform to create"""
        if self.current_height <= self.zone_thresholds['beginner'] / 20:  # 5% of beginner zone
            return None
            
        if random.random() >= self.moving_platform_chance:
            return None

        zone = self.get_current_zone()
        
        # Adjust speed distribution based on zone
        if zone == 'beginner':
            return 'moving_slow'
        elif zone == 'intermediate':
            return random.choice(['moving_slow', 'moving_medium'])
        elif zone == 'advanced':
            weights = [0.4, 0.4, 0.2]  # 40% slow, 40% medium, 20% fast
            return random.choices(
                ['moving_slow', 'moving_medium', 'moving_fast'],
                weights=weights
            )[0]
        else:  # expert
            weights = [0.2, 0.4, 0.4]  # 20% slow, 40% medium, 40% fast
            return random.choices(
                ['moving_slow', 'moving_medium', 'moving_fast'],
                weights=weights
            )[0]

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
                platform_type = self.get_platform_type()
                
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
