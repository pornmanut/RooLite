import pygame

class Camera:
    def __init__(self):
        self.offset_y = 0.0
        self.target_y = 0.0
        self.lerp_speed = 0.1  # Adjustable: 0.05-0.15 for smoother/faster movement
        
    def update(self, player_y, window_height):
        """Update camera position to smoothly follow the player"""
        # Target position keeps player slightly above center
        self.target_y = player_y - (window_height * 0.6)
        
        # Smooth camera movement using lerp
        self.offset_y += (self.target_y - self.offset_y) * self.lerp_speed
        
    def apply_offset(self, world_y):
        """Convert world coordinates to screen coordinates"""
        return world_y - self.offset_y
