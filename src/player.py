import pygame

class Player:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40
        self.x = float(x)  # Store as float for precise physics
        self.y = float(y)  # Store as float for precise physics
        self.velocity_y = 0.0
        self.velocity_x = 0.0
        self.speed = 5.0
        self.gravity = 0.5        # Matches main.py GRAVITY
        self.jump_force = -15.0   # Matches main.py JUMP_FORCE
        
        # Create a simple rectangle for now
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.color = (50, 120, 190)  # Blue-ish color

    def move(self, direction):
        """Handle horizontal movement"""
        self.velocity_x = direction * self.speed

    def update(self):
        """Update player position and apply physics"""
        # Apply gravity
        self.velocity_y += self.gravity
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Screen wrapping for horizontal movement
        if self.x < 0:
            self.x = 800 - self.width
        elif self.x > 800 - self.width:
            self.x = 0
            
        # Update rectangle position with integer coordinates
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def jump(self):
        """Make the player jump"""
        self.velocity_y = self.jump_force

    def render(self, screen):
        """Draw the player at current position"""
        self.render_at(screen, self.rect.x, self.rect.y)

    def render_at(self, screen, x, y):
        """Draw the player at specified screen coordinates"""
        draw_rect = pygame.Rect(int(x), int(y), self.width, self.height)
        pygame.draw.rect(screen, self.color, draw_rect)

    def check_platform_collision(self, platforms):
        """Check and handle collision with platforms"""
        for platform in platforms:
            if (self.velocity_y > 0 and  # Moving downward
                self.rect.bottom >= platform.rect.top and
                self.rect.bottom <= platform.rect.bottom and
                self.rect.right >= platform.rect.left and
                self.rect.left <= platform.rect.right):
                
                # Automatically jump when hitting a platform
                self.jump()
                platform.on_collision()  # Trigger platform disappearing effect
                return True
        return False
