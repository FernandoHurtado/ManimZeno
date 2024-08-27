from manim import *
from manim_mobject_svg import *

class PreciseFractionMarkersScene(Scene):
    def construct(self):
        # Create the number line (invisible, but needed for positioning)
        n_line = NumberLine(x_range=[0, 1], length=10, include_numbers=True).shift(UP*3)
        n_line.set_opacity(0)  # Make it invisible

        # Initialize an empty VGroup to hold all fraction markers
        fraction_markers = VGroup()

        # Function to calculate the points of division
        def get_division_points(depth, start=0, end=1):
            if depth == 0:
                return []
            else:
                mid = (start + end) / 2
                return [mid] + get_division_points(depth - 1, start, mid) + get_division_points(depth - 1, mid, end)

        # Set up parameters (exactly as in the full scene)
        recursive_depth = 8  # Keep this at 8 to maintain correct vertical spacing
        root_y = 2
        vertical_spacing = 0.525

        # Create fraction markers for all depth levels up to 6
        for i in range(1, recursive_depth + 1):
            points = get_division_points(i)
            if i <= 6:  # Only display fractions up to step 6
                fraction_size = max(0.15, 0.5 - 0.05 * i)
                for j in range(1, 2**i, 2):  # Place fractions only at the midpoint of each interval
                    fraction = MathTex(r"\frac{1}{" + str(2**i) + r"}", color=WHITE).scale(fraction_size)
                    # Position the fraction above the midpoint of the interval
                    fraction.move_to(n_line.number_to_point(j / 2**i) + DOWN * 1 - i * vertical_spacing * UP)
                    fraction_markers.add(fraction)

        # Add fraction markers to the scene
        self.add(fraction_markers)

        # Export the fraction markers as an SVG
        svg_path = fraction_markers.to_svg("precise_fraction_markers.svg", crop=False, padding=0.1)
        print(f"SVG file with precise fraction markers created at: {svg_path}")

if __name__ == "__main__":
    scene = PreciseFractionMarkersScene()
    scene.construct()
