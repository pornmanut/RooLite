import pygame
import sys
import random
from .player import Player
from .platform import Platform
from .camera import Camera
from .path_manager import PathManager

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Game physics constants
GRAVITY = 0.5
JUMP_FORCE = -15.0
MAX_JUMP_HEIGHT = (JUMP_FORCE ** 2) / (2 * GRAVITY)
PLATFORM_SPACING = MAX_JUMP_HEIGHT * 0.8
DIFFICULTY_HEIGHT = 2000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.max_height = 0
        
        # Initialize camera
        self.camera = Camera()
        
        # Initialize path manager
        self.path_manager = PathManager(WINDOW_WIDTH, PLATFORM_SPACING)
        
        # Create player at the center bottom of the screen
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        
        # Initialize platforms
        self.platforms = []
        self.generate_initial_platforms()

    def generate_initial_platforms(self):
        # Create starting platform under the player
        starting_platform = Platform(
            WINDOW_WIDTH // 2 - Platform.MAX_WIDTH // 2,
            WINDOW_HEIGHT - 50,
            difficulty=1.0,
            width=Platform.MAX_WIDTH
        )
        self.platforms.append(starting_platform)
        
        # Initialize path manager
        self.path_manager.initialize_path()
        
        # Generate initial platforms
        current_height = WINDOW_HEIGHT - 150
        spacing = PLATFORM_SPACING * 0.8
        
        while current_height > 0:
            # Get platform positions from path manager
            positions = self.path_manager.get_platform_positions(current_height)
            
            # Create platforms
            for pos in positions:
                platform = Platform(
                    pos['x'],
                    current_height,
                    difficulty=pos['difficulty']
                )
                platform.fade_duration = pos['fade_time']
                self.platforms.append(platform)
            
            # Move up to next height
            current_height -= spacing

    def add_platform(self):
        """Add new platform above the highest existing platform"""
        if not self.platforms:
            return
        
        # Find the highest platform
        highest_y = min(p.y for p in self.platforms)
        new_height = highest_y - PLATFORM_SPACING * 0.8
        
        # Get platform positions from path manager
        positions = self.path_manager.get_platform_positions(new_height)
        
        # Create new platforms
        for pos in positions:
            platform = Platform(
                pos['x'],
                new_height,
                difficulty=pos['difficulty']
            )
            platform.fade_duration = pos['fade_time']
            self.platforms.append(platform)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_LEFT]:
            direction = -1
        if keys[pygame.K_RIGHT]:
            direction = 1
        self.player.move(direction)

    def manage_platforms(self):
        # Remove platforms that are too far below view
        min_height = self.camera.offset_y + WINDOW_HEIGHT + 200
        self.platforms = [p for p in self.platforms 
                         if p.y < min_height]
        
        # Clean up path manager
        self.path_manager.cleanup(min_height)
        
        # Generate new platforms when approaching top of view
        highest_y = min(p.y for p in self.platforms) if self.platforms else 0
        screen_top = self.camera.offset_y - 100
        
        while highest_y > screen_top:
            self.add_platform()
            highest_y = min(p.y for p in self.platforms)

    def update(self):
        # Update player
        self.player.update()
        
        # Update camera to follow player
        self.camera.update(self.player.y, WINDOW_HEIGHT)
        
        # Update max height and score
        if -self.player.y > self.max_height:
            self.max_height = -self.player.y
            self.score = int(self.max_height)
        
        # Check collisions with platforms
        self.player.check_platform_collision(self.platforms)
        
        # Update platforms
        for platform in self.platforms[:]:
            platform.update()
            if not platform.active:
                self.platforms.remove(platform)
                self.add_platform()
        
        self.manage_platforms()
        
        if self.camera.apply_offset(self.player.y) > WINDOW_HEIGHT + 100:
            self.running = False

    def render(self):
        self.screen.fill(WHITE)
        
        # Draw platforms
        for platform in self.platforms:
            screen_y = self.camera.apply_offset(platform.y)
            if -50 <= screen_y <= WINDOW_HEIGHT + 50:
                platform.render_at(self.screen, platform.x, screen_y)
        
        # Draw player
        screen_y = self.camera.apply_offset(self.player.y)
        self.player.render_at(self.screen, self.player.x, screen_y)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
