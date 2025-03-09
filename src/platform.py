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
        'normal': (34, 139, 34),    # Green
        'small': (139, 69, 19),     # Brown
        'medium': (34, 139, 34),    # Green
        'large': (0, 100, 0)        # Dark Green
    }

    def __init__(self, x, y, difficulty=1.0, width=None):
        # Determine platform width based on difficulty
        if width is None:
            base_width = self.MAX_WIDTH - (difficulty * 15)  # Platforms get smaller with difficulty
            width_variation = random.randint(-10, 10)  # Add some randomness
            self.width = max(self.MIN_WIDTH, min(self.MAX_WIDTH, base_width + width_variation))
        else:
            self.width = width

        self.height = self.DEFAULT_HEIGHT
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Set color based on platform size
        if self.width <= 70:
            self.platform_type = 'small'
        elif self.width <= 85:
            self.platform_type = 'medium'
        else:
            self.platform_type = 'large'
        
        self.color = self.COLORS[self.platform_type]
        
        self.active = True
        self.disappear_timer = None
        self.fade_duration = 2.0  # Default fade duration
        self.alpha = 255

    def on_collision(self):
        """Called when player collides with platform"""
        if self.active and not self.disappear_timer:
            self.disappear_timer = time.time()

    def update(self):
        """Update platform state"""
        if self.disappear_timer:
            elapsed = time.time() - self.disappear_timer
            if elapsed >= self.fade_duration:
                self.active = False
            else:
                # Calculate alpha based on elapsed time
                self.alpha = 255 * (1 - (elapsed / self.fade_duration))
        
        # Update rectangle position
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
            # Create a surface with alpha channel
            platform_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            color_with_alpha = (*self.color, int(self.alpha))
            pygame.draw.rect(platform_surface, color_with_alpha, 
                           (0, 0, self.width, self.height))
            screen.blit(platform_surface, (x, y))
        else:
            draw_rect = pygame.Rect(int(x), int(y), self.width, self.height)
            pygame.draw.rect(screen, self.color, draw_rect)

    @property
    def is_small(self):
        """Check if this is a small platform"""
        return self.platform_type == 'small'

    @property
    def is_large(self):
        """Check if this is a large platform"""
        return self.platform_type == 'large'
