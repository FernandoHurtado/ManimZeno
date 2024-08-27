from manim import *
from manim_mobject_svg import *

class StaticManimScene(Scene):
    def construct(self):
        # Create the number line
        n_line = NumberLine(x_range=[0, 1], length=10, include_numbers=True).shift(UP*3)

        # Initialize an empty VGroup to hold all parts of the tree
        tree = VGroup()

        # Function to calculate the points of division
        def get_division_points(depth, start=0, end=1):
            if depth == 0:
                return []
            else:
                mid = (start + end) / 2
                return [mid] + get_division_points(depth - 1, start, mid) + get_division_points(depth - 1, mid, end)

        # Function to create division marks with decreasing size 
        def create_division_marks(points, depth):
            marks = VGroup()
            length_factor = max(0.2, 3 - (depth * 0.5))
            width_factor = max(2, 4 - (depth * 0.5))
            for point in points:
                mark = Line(
                    start=n_line.number_to_point(point) + UP * 0.2 * length_factor,
                    end=n_line.number_to_point(point) + DOWN * 0.2 * length_factor,
                    stroke_width=width_factor
                )
                marks.add(mark)
            return marks

        # Function to add nodes and edges to the tree with decreasing size
        def add_to_tree(nodes, edges, depth, x_pos, y_pos, space, vertical_spacing, edge_width, node_size):
            if depth == 0:
                return
            else:
                left_x = x_pos - space / 2
                right_x = x_pos + space / 2
                new_y = y_pos - vertical_spacing

                left_node = Dot(point=np.array([left_x, new_y, 0]), radius=node_size)
                right_node = Dot(point=np.array([right_x, new_y, 0]), radius=node_size)
                nodes.add(left_node, right_node)

                left_edge = Line(start=np.array([x_pos, y_pos, 0]), end=left_node.get_center(), stroke_width=edge_width)
                right_edge = Line(start=np.array([x_pos, y_pos, 0]), end=right_node.get_center(), stroke_width=edge_width)
                edges.add(left_edge, right_edge)

                # Recursive calls for left and right children with adjusted edge width and node size
                add_to_tree(nodes, edges, depth - 1, left_x, new_y, space / 2, vertical_spacing, edge_width * 0.95, node_size * 0.85)
                add_to_tree(nodes, edges, depth - 1, right_x, new_y, space / 2, vertical_spacing, edge_width * 0.95, node_size * 0.85)

        # Set up parameters
        recursive_depth = 8
        root_x = 0
        root_y = 2
        initial_space = 5
        initial_edge_width = 3
        initial_node_size = 0.1
        vertical_spacing = 0.525

        # Create the root node and add to the tree VGroup
        root_node = Dot(point=np.array([root_x, root_y, 0]), radius=initial_node_size)
        tree.add(root_node)

        # Create division marks and tree nodes for all depth levels
        for i in range(1, recursive_depth + 1):
            points = get_division_points(i)
            marks = create_division_marks(points, i)
            tree.add(marks)

            # Add nodes and edges to the tree
            nodes = VGroup(root_node)
            edges = VGroup()
            add_to_tree(nodes, edges, i, root_x, root_y, initial_space, vertical_spacing, initial_edge_width, initial_node_size)
            tree.add(nodes, edges)

            # Add step number and the number of parts at each step
            step_number = MathTex(f"{i}", color=WHITE).scale(0.7)
            parts_number = MathTex(r"2^{" + f"{i}" + r"}", color=WHITE).scale(0.7)

            # Position step number and parts number to the left of the binary tree
            step_number.move_to(np.array([-6.5, root_y - (i - 1) * vertical_spacing - 0.5, 0]))
            parts_number.move_to(np.array([-6, root_y - (i - 1) * vertical_spacing - 0.5, 0]))

            tree.add(step_number, parts_number)

        # Create the set representation with large brackets
        set_width = 10
        set_bracket_left = MathTex(r"\{").scale(2)
        set_bracket_right = MathTex(r"\}").scale(2)
        center_point = n_line.get_center()
        set_bracket_left.move_to(center_point + DOWN*6 + LEFT*(set_width/2))
        set_bracket_right.move_to(center_point + DOWN*6 + RIGHT*(set_width/2))

        # Create the omega symbol and the "2^ℕ" notation
        omega_symbol = MathTex(r"\omega").scale(0.7)
        two_to_the_n_symbol = MathTex(r"2^{\mathbb{N}}").scale(0.7)

        # Position the omega symbol and the "2^ℕ" notation
        omega_symbol.move_to(np.array([-6.5, set_bracket_left.get_y(), 0]))
        two_to_the_n_symbol.move_to(np.array([-6, set_bracket_right.get_y(), 0]))

        # Create the ellipsis that indicates the continuation of the process
        continuation_dots = MathTex(r"\cdots").next_to(tree, DOWN, buff=0.5)
        left_continuation_dots = MathTex(r"\cdots")
        left_continuation_dots.move_to(np.array([-6.25, continuation_dots.get_center()[1], 0]))

        # Add all elements to the scene
        all_elements = VGroup(n_line, tree, set_bracket_left, set_bracket_right, omega_symbol, two_to_the_n_symbol, continuation_dots, left_continuation_dots)
        self.add(all_elements)

        # Export the entire scene as an SVG
        svg_path = all_elements.to_svg("zeno_measure_tree.svg", crop=False, padding=0.1)
        print(f"SVG file created at: {svg_path}")

if __name__ == "__main__":
    scene = StaticManimScene()
    scene.construct()
