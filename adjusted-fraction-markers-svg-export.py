from manim import *
from manim_mobject_svg import *

class AdjustedFractionMarkersScene(Scene):
    def construct(self):
        # Create the number line (invisible, but needed for positioning)
        n_line = NumberLine(x_range=[0, 1], length=10, include_numbers=True).shift(UP*3)
        n_line.set_opacity(0)  # Make it invisible

        # Initialize an empty VGroup to hold all fraction markers
        fraction_markers = VGroup()

        # Set up parameters
        recursive_depth = 8  # Keep this at 8 to maintain correct vertical spacing
        root_y = 2
        vertical_spacing = 0.525

        # Create fraction markers for all depth levels
        for i in range(2, recursive_depth + 1):  # Start from 2 to skip the root node
            fraction_size = max(0.15, 0.5 - 0.05 * i)
            for j in range(2**i):  # Place fractions at all points in this level
                fraction = MathTex(r"\frac{1}{" + str(2**(i-1)) + r"}", color=WHITE).scale(fraction_size)
                # Position the fraction above each point in the level
                fraction.move_to(n_line.number_to_point(j / (2**i)) + DOWN * 1 - i * vertical_spacing * UP)
                fraction_markers.add(fraction)

            if i == 7:  # Stop after placing 1/64 fractions
                break

        # Add fraction markers to the scene
        self.add(fraction_markers)

        # Export the fraction markers as an SVG
        svg_path = fraction_markers.to_svg("adjusted_fraction_markers.svg", crop=False, padding=0.1)
        print(f"SVG file with adjusted fraction markers created at: {svg_path}")

if __name__ == "__main__":
    scene = AdjustedFractionMarkersScene()
    scene.construct()
