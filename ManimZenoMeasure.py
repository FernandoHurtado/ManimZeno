from manim import *

class ManimMeasure(Scene):
    def construct(self):
        n_line = NumberLine(x_range=[0, 1], length=10, include_numbers=True)
        self.play(Create(n_line))

        self.wait(2)

        # Function to calculate the points of division
        def get_division_points(depth, start=0, end=1):
            if depth == 0:
                return []
            else:
                mid = (start + end) / 2
                return [mid] + get_division_points(depth - 1, start, mid) + get_division_points(depth - 1, mid, end)

        # Function to create division marks with decreasing size more aggressively
        def create_division_marks(points, depth):
            marks = []
            # Adjust these factors to make the marks thinner and longer
            length_factor = max(0.5, 3 - (depth * 0.5))  # Ensure length_factor doesn't go below a threshold
            width_factor = max(2, 4 - (depth * 0.5))  # Ensure width_factor doesn't become too thin
            for point in points:
                mark = Line(
                    start=n_line.number_to_point(point) + UP * 0.2 * length_factor,
                    end=n_line.number_to_point(point) + DOWN * 0.2 * length_factor,
                    stroke_width=width_factor
                )
                marks.append(mark)
            return marks

        # Recursive depth for simultaneous divisions
        recursive_depth = 8  # You can change the depth as needed
        animation_speed = 0.5  # Set a constant animation speed

        # Create and animate division marks at each depth level
        for i in range(1, recursive_depth + 1):
            points = get_division_points(i)
            marks = create_division_marks(points, i)
            # Use a fixed run_time for a consistent animation speed
            self.play(*[Create(mark) for mark in marks], run_time=animation_speed)
            self.wait(1)  # Consistent wait time between levels

        self.wait(1)