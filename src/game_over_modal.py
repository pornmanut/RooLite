import pygame
from typing import List, Tuple, Optional, Callable
from .high_scores import HighScore, HighScoreManager

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 color: Tuple[int, int, int], hover_color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)  # border
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class GameOverModal:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False
        self.score = 0
        self.high_scores: List[HighScore] = []
        self.input_active = False
        self.player_name = ""
        self.needs_name_input = False
        self.manager = HighScoreManager()
        self.default_name = "Unknown"
        
        # Modal dimensions
        self.width = 600
        self.height = 500
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Colors
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.input_color = (220, 220, 220)
        self.hint_color = (128, 128, 128)  # Gray color for placeholder text
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.score_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        
        # Layout calculations
        self.content_margin = 20
        self.section_spacing = 20
        self.high_score_spacing = 25
        
        # Input box dimensions
        self.input_box_width = 200
        self.input_box_height = 30
        
        # Button dimensions
        self.button_width = 120
        self.button_height = 40
        self.button_spacing = 40
        
        # Reserve space for UI elements
        self.title_height = 48
        self.score_height = 36
        self.high_scores_header_height = 36
        self.high_scores_list_height = self.high_score_spacing * 10
        self.input_section_height = self.input_box_height + 30
        
        # Calculate fixed positions for bottom elements
        self.bottom_margin = 30
        button_y = self.y + self.height - self.button_height - self.bottom_margin
        
        self.retry_button = Button(
            self.x + (self.width // 2) - self.button_width - self.button_spacing,
            button_y,
            self.button_width,
            self.button_height,
            "Retry",
            (150, 255, 150),
            (100, 200, 100)
        )
        
        self.quit_button = Button(
            self.x + (self.width // 2) + self.button_spacing,
            button_y,
            self.button_width,
            self.button_height,
            "Quit",
            (255, 150, 150),
            (200, 100, 100)
        )

    def show(self, score: int) -> None:
        self.visible = True
        self.score = score
        self.high_scores = self.manager.get_scores()
        self.needs_name_input = self.manager.is_high_score(score)
        self.input_active = self.needs_name_input
        self.player_name = ""

    def hide(self) -> None:
        self.visible = False
        self.input_active = False
        self.player_name = ""

    def _save_score(self) -> None:
        """Save the score with either the entered name or default name"""
        name = self.player_name.strip() if self.player_name.strip() else self.default_name
        self.manager.add_score(name, self.score)

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if not self.visible:
            return None

        if self.retry_button.handle_event(event):
            if self.needs_name_input:
                self._save_score()
            return "retry"
            
        if self.quit_button.handle_event(event):
            if self.needs_name_input:
                self._save_score()
            return "quit"

        if self.needs_name_input and self.input_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.player_name.strip():
                        self.player_name = self.default_name
                    self.input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.unicode.isprintable():  # Only accept printable characters
                    if len(self.player_name) < 20:  # Max name length
                        self.player_name += event.unicode

        return None

    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return

        # Draw semi-transparent background
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 128), s.get_rect())
        surface.blit(s, (0, 0))

        # Draw modal background
        pygame.draw.rect(surface, self.bg_color, 
                        (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.text_color, 
                        (self.x, self.y, self.width, self.height), 2)

        # Start drawing from top with fixed content_margin
        current_y = self.y + self.content_margin

        # Draw title
        title = self.title_font.render("Game Over!", True, self.text_color)
        title_rect = title.get_rect(centerx=self.x + self.width // 2, 
                                  top=current_y)
        surface.blit(title, title_rect)
        current_y += self.title_height + self.section_spacing

        # Draw current score
        score_text = self.score_font.render(f"Your Score: {self.score}", 
                                          True, self.text_color)
        score_rect = score_text.get_rect(centerx=self.x + self.width // 2, 
                                       top=current_y)
        surface.blit(score_text, score_rect)
        current_y += self.score_height + self.section_spacing

        # Draw high scores header
        header = self.score_font.render("High Scores", True, self.text_color)
        header_rect = header.get_rect(centerx=self.x + self.width // 2, 
                                    top=current_y)
        surface.blit(header, header_rect)
        current_y += self.high_scores_header_height + self.section_spacing
        
        # Draw high scores
        score_start_x = self.x + 50
        for i, score in enumerate(self.high_scores[:10]):
            score_line = self.text_font.render(
                f"{i+1}. {score.player_name} - {score.score}", 
                True, self.text_color
            )
            surface.blit(score_line, (score_start_x, current_y))
            current_y += self.high_score_spacing
        
        # Add spacing after high scores list
        current_y += self.section_spacing

        # Draw name input if needed
        if self.needs_name_input:
            # Calculate remaining space and center input section
            space_for_input = (self.y + self.height - self.bottom_margin - 
                             self.button_height - current_y - self.input_section_height)
            input_y = current_y + (space_for_input // 2)
            
            prompt = self.text_font.render("Enter your name:", 
                                         True, self.text_color)
            surface.blit(prompt, (score_start_x, input_y))
            input_y += 25  # Space for prompt text
            
            input_rect = pygame.Rect(score_start_x, 
                                   input_y,
                                   self.input_box_width, 
                                   self.input_box_height)
            pygame.draw.rect(surface, self.input_color, input_rect)
            pygame.draw.rect(surface, self.text_color, input_rect, 1)
            
            # Draw the name or placeholder
            if self.player_name:
                name_surface = self.text_font.render(self.player_name, 
                                                   True, self.text_color)
            else:
                name_surface = self.text_font.render("Type your name...", 
                                                   True, self.hint_color)
            
            surface.blit(name_surface, (input_rect.x + 5, input_rect.y + 5))
            
            if self.input_active:
                cursor_x = input_rect.x + 5 + name_surface.get_width()
                pygame.draw.line(surface, self.text_color,
                               (cursor_x, input_rect.y + 5),
                               (cursor_x, input_rect.y + 25))

        # Draw buttons (already positioned at fixed locations)
        self.retry_button.draw(surface)
        self.quit_button.draw(surface)
