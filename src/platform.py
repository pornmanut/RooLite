import pygame
import time
import random

class Platform:
    # Platform size constants
    MIN_WIDTH = 60
    MAX_WIDTH = 100
    DEFAULT_HEIGHT = 20
    
    # Color variations for different platform types
    COLORS = {
        'normal': (34, 139, 34),     # Green
        'small': (139, 69, 19),      # Brown
        'medium': (34, 139, 34),     # Green
        'large': (0, 100, 0),        # Dark Green
        'moving_slow': (135, 206, 235),    # Sky Blue
        'moving_medium': (0, 191, 255),    # Deep Sky Blue
        'moving_fast': (30, 144, 255)      # Bright Blue
    }
    
    # Movement speeds for different types
    SPEEDS = {
        'moving_slow': 1.5,     # Slow speed
        'moving_medium': 2.5,   # Medium speed
        'moving_fast': 3.5      # Fast speed
    }
    
    # Movement ranges
    RANGES = {
        'moving_slow': 50,      # Shorter range
        'moving_medium': 70,    # Medium range
        'moving_fast': 90       # Longer range
    }

    def __init__(self, x, y, difficulty=1.0, width=None, platform_type='normal'):
        # Determine platform width based on difficulty
        if width is None:
            base_width = self.MAX_WIDTH - (difficulty * 15)
            width_variation = random.randint(-10, 10)
            self.width = max(self.MIN_WIDTH, min(self.MAX_WIDTH, base_width + width_variation))
        else:
            self.width = width

        self.height = self.DEFAULT_HEIGHT
        self.x = float(x)
        self.y = y
        self.start_x = x
        
        # Movement properties
        self.is_moving = platform_type.startswith('moving_')
        if self.is_moving:
            base_speed = self.SPEEDS.get(platform_type, 2.5)
            base_range = self.RANGES.get(platform_type, 70)
            # Add slight randomness to speed and range
            self.move_speed = base_speed + (random.random() * 0.5 - 0.25)
            self.move_range = base_range + random.randint(-10, 10)
            # Apply difficulty scaling but with less impact
            self.move_speed += difficulty * 0.5
            self.move_range += difficulty * 10
        else:
            self.move_speed = 0
            self.move_range = 0
            
        self.direction = 1
        
        # Initialize rect
        self.rect = pygame.Rect(int(x), y, self.width, self.height)
        
        # Set platform type and color
        self.platform_type = platform_type
        self.color = self.COLORS.get(platform_type, self.COLORS['normal'])
        self.fade_duration = 1.5 if self.is_moving else 2.0
        
        self.active = True
        self.disappear_timer = None
        self.alpha = 255
        
        self._alpha_surface = None
        self._direction_indicator = None

    def _create_alpha_surface(self):
        """Create alpha surface only when needed"""
        if self._alpha_surface is None:
            self._alpha_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        return self._alpha_surface

    def _create_direction_indicator(self):
        """Create direction indicator for moving platforms"""
        if not self.is_moving or self._direction_indicator is not None:
            return
            
        indicator_width = 24
        indicator_height = 8
        surface = pygame.Surface((indicator_width, indicator_height), pygame.SRCALPHA)
        
        if self.direction > 0:  # Right arrow
            points = [(0, 4), (16, 4), (16, 0), (24, 4), (16, 8), (16, 4)]
        else:  # Left arrow
            points = [(24, 4), (8, 4), (8, 0), (0, 4), (8, 8), (8, 4)]
            
        pygame.draw.polygon(surface, (*self.color, 200), points)
        pygame.draw.polygon(surface, (255, 255, 255, 100), points, 1)
        
        self._direction_indicator = surface
        return surface

    def on_collision(self):
        """Called when player collides with platform (renamed from collision)"""
        if self.active and not self.disappear_timer:
            self.disappear_timer = time.time()

    def update(self):
        """Update platform state"""
        if self.is_moving and self.active:
            self.x += self.move_speed * self.direction
            
            if abs(self.x - self.start_x) > self.move_range:
                self.direction *= -1
                self._direction_indicator = None
        
        if self.disappear_timer:
            elapsed = time.time() - self.disappear_timer
            if elapsed >= self.fade_duration:
                self.active = False
                self._alpha_surface = None
                self._direction_indicator = None
            else:
                self.alpha = 255 * (1 - (elapsed / self.fade_duration))
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def render(self, screen):
        """Draw the platform at its current position"""
        self.render_at(screen, self.x, self.y)

    def render_at(self, screen, x, y):
        """Draw the platform at specified screen coordinates"""
        if not self.active:
            return

        if self.disappear_timer:
            surface = self._create_alpha_surface()
            color_with_alpha = (*self.color, int(self.alpha))
            surface.fill((0, 0, 0, 0))
            pygame.draw.rect(surface, color_with_alpha, 
                           (0, 0, self.width, self.height))
            screen.blit(surface, (int(x), int(y)))
            
            if self.is_moving and self.alpha > 50:
                indicator = self._create_direction_indicator()
                if indicator:
                    indicator.set_alpha(int(self.alpha))
                    screen.blit(indicator, (int(x) + self.width//2 - 12, int(y) - 10))
        else:
            draw_rect = pygame.Rect(int(x), int(y), self.width, self.height)
            pygame.draw.rect(screen, self.color, draw_rect)
            
            if self.is_moving:
                indicator = self._create_direction_indicator()
                if indicator:
                    screen.blit(indicator, (int(x) + self.width//2 - 12, int(y) - 10))

    def cleanup(self):
        """Clean up platform resources"""
        self.active = False
        self._alpha_surface = None
        self._direction_indicator = None

    def __del__(self):
        """Ensure resources are cleaned up"""
        self.cleanup()
