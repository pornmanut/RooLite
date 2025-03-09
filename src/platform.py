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
            base_width = self.MAX_WIDTH - (difficulty * 15)
            width_variation = random.randint(-10, 10)
            self.width = max(self.MIN_WIDTH, min(self.MAX_WIDTH, base_width + width_variation))
        else:
            self.width = width

        self.height = self.DEFAULT_HEIGHT
        self.x = x
        self.y = y
        
        # Initialize rect without creating a new surface
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
        self.fade_duration = 2.0
        self.alpha = 255
        
        # Cache for alpha surface
        self._alpha_surface = None

    def _create_alpha_surface(self):
        """Create alpha surface only when needed"""
        if self._alpha_surface is None:
            self._alpha_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        return self._alpha_surface

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
                # Clear cached surface when platform becomes inactive
                self._alpha_surface = None
            else:
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
            # Use cached alpha surface
            surface = self._create_alpha_surface()
            color_with_alpha = (*self.color, int(self.alpha))
            surface.fill((0, 0, 0, 0))  # Clear surface
            pygame.draw.rect(surface, color_with_alpha, 
                           (0, 0, self.width, self.height))
            screen.blit(surface, (x, y))
        else:
            draw_rect = pygame.Rect(int(x), int(y), self.width, self.height)
            pygame.draw.rect(screen, self.color, draw_rect)

    def cleanup(self):
        """Clean up platform resources"""
        self.active = False
        if self._alpha_surface:
            self._alpha_surface = None

    def __del__(self):
        """Ensure resources are cleaned up"""
        self.cleanup()
