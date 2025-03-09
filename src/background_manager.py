class BackgroundManager:
    # Base zone colors
    BEGINNER_START = (152, 251, 152)    # Pale Green
    BEGINNER_END = (0, 178, 238)        # Sky Blue
    
    INTERMEDIATE_START = (0, 178, 238)   # Sky Blue
    INTERMEDIATE_END = (147, 112, 219)   # Medium Purple
    
    ADVANCED_START = (147, 112, 219)     # Medium Purple
    ADVANCED_END = (178, 34, 34)         # Firebrick Red
    
    EXPERT_START = (178, 34, 34)         # Firebrick Red
    EXPERT_END = (25, 25, 112)          # Midnight Blue

    def __init__(self):
        # Define zone boundaries and colors
        self.transition_points = [
            # Beginner Zone (0-10000)
            (0, self.BEGINNER_START),
            (5000, self.BEGINNER_END),
            
            # Intermediate Zone (10001-40000)
            (10000, self.INTERMEDIATE_START),
            (25000, self.INTERMEDIATE_END),
            
            # Advanced Zone (40001-80000)
            (40000, self.ADVANCED_START),
            (60000, self.ADVANCED_END),
            
            # Expert Zone (80001+)
            (80000, self.EXPERT_START),
            (100000, self.EXPERT_END)
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
