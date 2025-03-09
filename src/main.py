import pygame
import sys
import random
from .player import Player
from .platform import Platform
from .camera import Camera
from .path_manager import PathManager
from .background_manager import BackgroundManager
from .game_over_modal import GameOverModal

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

# Memory management constants
CLEANUP_BUFFER = WINDOW_HEIGHT * 2
MAX_PLATFORMS = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        self.max_height = 0
        
        # Initialize managers
        self.camera = Camera()
        self.path_manager = PathManager(WINDOW_WIDTH, PLATFORM_SPACING)
        self.background_manager = BackgroundManager()
        
        # Initialize game over modal
        self.game_over_modal = GameOverModal(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Create player at the center bottom of the screen
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        
        # Initialize platforms
        self.platforms = []
        self.inactive_platforms = []
        self.generate_initial_platforms()

    def generate_initial_platforms(self):
        # Create starting platform under the player
        starting_platform = Platform(
            WINDOW_WIDTH // 2 - Platform.MAX_WIDTH // 2,
            WINDOW_HEIGHT - 50,
            difficulty=1.0,
            width=Platform.MAX_WIDTH,
            platform_type='normal'  # First platform is always static
        )
        self.platforms.append(starting_platform)
        
        # Initialize path manager
        self.path_manager.initialize_path()
        
        # Generate initial platforms
        current_height = WINDOW_HEIGHT - 150
        spacing = PLATFORM_SPACING * 0.8
        
        while current_height > 0:
            positions = self.path_manager.get_platform_positions(current_height)
            for pos in positions:
                platform = Platform(
                    pos['x'],
                    current_height,
                    difficulty=pos['difficulty'],
                    platform_type=pos['platform_type']
                )
                platform.fade_duration = pos['fade_time']
                self.platforms.append(platform)
            current_height -= spacing

    def cleanup_platforms(self):
        """Remove platforms that are too far below view or inactive"""
        min_height = self.camera.offset_y + WINDOW_HEIGHT + CLEANUP_BUFFER
        
        # Move inactive platforms to separate list
        active_platforms = []
        for platform in self.platforms:
            if not platform.active:
                self.inactive_platforms.append(platform)
            elif platform.y < min_height:
                active_platforms.append(platform)
                
        self.platforms = active_platforms
        
        # Clean up inactive platforms
        self.inactive_platforms = [p for p in self.inactive_platforms 
                                if p.alpha > 0 and p.y < min_height]
        
        # Enforce maximum platform limit
        if len(self.platforms) > MAX_PLATFORMS:
            self.platforms.sort(key=lambda p: p.y)
            self.platforms = self.platforms[:MAX_PLATFORMS]

    def add_platform(self):
        """Add new platform above the highest existing platform"""
        if not self.platforms:
            return
        
        highest_y = min(p.y for p in self.platforms)
        new_height = highest_y - PLATFORM_SPACING * 0.8
        
        positions = self.path_manager.get_platform_positions(new_height)
        for pos in positions:
            platform = Platform(
                pos['x'],
                new_height,
                difficulty=pos['difficulty'],
                platform_type=pos['platform_type']
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
            
            # Handle game over modal events
            if self.game_over:
                action = self.game_over_modal.handle_event(event)
                if action == "retry":
                    self.reset_game()
                elif action == "quit":
                    self.running = False
                continue

        if not self.game_over:
            keys = pygame.key.get_pressed()
            direction = 0
            if keys[pygame.K_LEFT]:
                direction = -1
            if keys[pygame.K_RIGHT]:
                direction = 1
            self.player.move(direction)

    def reset_game(self):
        """Reset the game state for a new game"""
        self.game_over = False
        self.score = 0
        self.max_height = 0
        self.camera = Camera()
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        self.platforms.clear()
        self.inactive_platforms.clear()
        self.generate_initial_platforms()

    def manage_platforms(self):
        # Clean up platforms periodically
        self.cleanup_platforms()
        
        # Generate new platforms when approaching top of view
        if self.platforms:
            highest_y = min(p.y for p in self.platforms)
            screen_top = self.camera.offset_y - 100
            
            while highest_y > screen_top:
                self.add_platform()
                highest_y = min(p.y for p in self.platforms)

    def update(self):
        if self.game_over:
            return

        # Update player
        self.player.update()
        
        # Update camera to follow player
        self.camera.update(self.player.y, WINDOW_HEIGHT)
        
        # Update max height and score
        if -self.player.y > self.max_height:
            self.max_height = -self.player.y
            self.score = int(self.max_height)
        
        # Check collisions with active platforms
        self.player.check_platform_collision(self.platforms)
        
        # Update all platforms
        for platform in self.inactive_platforms:
            platform.update()
        for platform in self.platforms:
            platform.update()
        
        self.manage_platforms()
        
        # Check for game over
        if self.camera.apply_offset(self.player.y) > WINDOW_HEIGHT + 100:
            self.game_over = True
            self.game_over_modal.show(self.score)

    def render(self):
        # Get background color based on score
        bg_color = self.background_manager.get_background_color(self.score)
        self.screen.fill(bg_color)
        
        # Draw inactive platforms first
        for platform in self.inactive_platforms:
            screen_y = self.camera.apply_offset(platform.y)
            if -50 <= screen_y <= WINDOW_HEIGHT + 50:
                platform.render_at(self.screen, platform.x, screen_y)
        
        # Draw active platforms
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

        # Draw game over modal if needed
        if self.game_over:
            self.game_over_modal.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
    def __del__(self):
        """Cleanup when game object is destroyed"""
        self.platforms.clear()
        self.inactive_platforms.clear()

def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
