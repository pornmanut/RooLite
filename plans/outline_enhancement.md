# Outline Enhancement Plan

## Overview
Add outlines to player and platform sprites to improve visibility against similar background colors.

## Implementation Plan

### 1. Player Outline Implementation
```mermaid
graph TD
    A[Current Player Render] -->|Modify| B[Add Outline]
    B --> C[Draw filled rectangle]
    B --> D[Draw outline rectangle]
    D --> E[Outline color based on player color]
    D --> F[Configurable outline thickness]
```

Changes needed in `player.py`:
- Add outline_thickness parameter (default: 2)
- Add outline_color calculation (will be a contrasting color to player.color)
- Modify render_at method to draw both fill and outline

### 2. Platform Outline Implementation
```mermaid
graph TD
    A[Current Platform Render] -->|Modify| B[Add Outline]
    B --> C[Handle Normal State]
    B --> D[Handle Fading State]
    C --> E[Draw filled rectangle]
    C --> F[Draw outline rectangle]
    D --> G[Draw with alpha surface]
    D --> H[Draw outline with alpha]
```

Changes needed in `platform.py`:
- Add outline_thickness parameter (default: 2)
- Add outline_color calculation for each platform type
- Modify render_at method to handle outlines in both normal and fading states

### 3. Color Contrast Algorithm
```mermaid
graph TD
    A[Input Color] -->|Calculate| B[Brightness]
    B -->|Check| C{Is Dark?}
    C -->|Yes| D[Light Outline]
    C -->|No| E[Dark Outline]
```

Implementation approach:
1. Calculate relative luminance of the fill color
2. Choose white outline for dark colors
3. Choose black outline for light colors

## Technical Specifications

### Player Class Changes
```python
def render_at(self, screen, x, y):
    # Inner fill
    draw_rect = pygame.Rect(int(x), int(y), self.width, self.height)
    pygame.draw.rect(screen, self.color, draw_rect)
    # Outer outline
    pygame.draw.rect(screen, outline_color, draw_rect, outline_thickness)
```

### Platform Class Changes
```python
def render_at(self, screen, x, y):
    if self.disappear_timer:
        # Handle fading with outline
        surface = self._create_alpha_surface()
        # Draw fill and outline on alpha surface
    else:
        # Draw normal platform with outline
