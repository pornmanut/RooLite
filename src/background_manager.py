class BackgroundManager:
    # Color definitions
    LIGHT_BLUE = (135, 206, 235)
    DARK_BLUE = (0, 0, 139)
    PURPLE = (128, 0, 128)
    DARK_PURPLE = (48, 0, 48)
    BLACK = (0, 0, 0)

    def __init__(self):
        # Define color transition points
        self.transition_points = [
            (0, self.LIGHT_BLUE),
            (12500, self.DARK_BLUE),
            (25000, self.PURPLE),
            (37500, self.DARK_PURPLE),
            (50000, self.BLACK)
        ]

    def interpolate_color(self, color1, color2, factor):
        """
        Interpolate between two colors.
        factor: 0.0 to 1.0 representing transition progress
        """
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        return (r, g, b)

    def get_background_color(self, score):
        """
        Get the background color based on the current score.
        """
        # Handle scores beyond the maximum transition point
        if score >= self.transition_points[-1][0]:
            return self.transition_points[-1][1]

        # Find the appropriate color transition segment
        for i in range(len(self.transition_points) - 1):
            start_score, start_color = self.transition_points[i]
            end_score, end_color = self.transition_points[i + 1]

            if start_score <= score < end_score:
                # Calculate transition progress
                progress = (score - start_score) / (end_score - start_score)
                return self.interpolate_color(start_color, end_color, progress)

        # Default to initial color if score is below first transition
        return self.transition_points[0][1]
