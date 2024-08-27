from manim import *
from manim_mobject_svg import *

class AdjustedFractionMarkersScene(Scene):
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

        # Set up parameters
        recursive_depth = 8
        root_x = 0
        root_y = 2
        vertical_spacing = 0.525

        # Add 'X' to the root node
        root_x = MathTex("X", color=WHITE).scale(0.7)
        root_x.move_to(np.array([root_x, root_y, 0]))
        fraction_markers.add(root_x)

        # Create fraction markers for all depth levels up to 7 (shifted down by one level)
        for i in range(1, recursive_depth + 1):
            points = get_division_points(i)
            if i <= 7:  # Display fractions up to step 7 (equivalent to step 6 in the original)
                fraction_size = max(0.15, 0.5 - 0.05 * i)
                for j in range(2**i):  # Place fractions at all points of this level
                    fraction = MathTex(r"\frac{1}{" + str(2**(i-1)) + r"}", color=WHITE).scale(fraction_size)
                    # Position the fraction, shifted down by one level
                    fraction.move_to(n_line.number_to_point(j / 2**i) + DOWN * 1 - i * vertical_spacing * UP)
                    fraction_markers.add(fraction)

        # Add fraction markers to the scene
        self.add(fraction_markers)

        # Export the fraction markers as an SVG
        svg_path = fraction_markers.to_svg("adjusted_fraction_markers.svg", crop=False, padding=0.1)
        print(f"SVG file with adjusted fraction markers created at: {svg_path}")

if __name__ == "__main__":
    scene = AdjustedFractionMarkersScene()
    scene.construct()
