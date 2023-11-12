from manim import *

class ManimMeasureTree(Scene):
    def construct(self):
        n_line = NumberLine(x_range=[0, 1], length=10, include_numbers=True).shift(UP*3)
        self.play(Create(n_line))

        self.wait(2)

        # Initialize an empty VGroup to hold all parts of the tree
        tree = VGroup()

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
            length_factor = max(0.5, 3 - (depth * 0.5))
            width_factor = max(2, 4 - (depth * 0.5))
            for point in points:
                mark = Line(
                    start=n_line.number_to_point(point) + UP * 0.2 * length_factor,
                    end=n_line.number_to_point(point) + DOWN * 0.2 * length_factor,
                    stroke_width=width_factor
                )
                marks.append(mark)
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

        # Recursive depth for simultaneous divisions
        recursive_depth = 8
        animation_speed = 0.5

        # Coordinates for the root of the binary tree
        root_x = 0
        root_y = 2
        initial_space = 5

        # Initial edge width and node size
        initial_edge_width = 3
        initial_node_size = 0.1

        # Create the root node and add to the tree VGroup
        root_node = Dot(point=np.array([root_x, root_y, 0]), radius=initial_node_size)
        tree.add(root_node)

        # Create and animate division marks and tree nodes at each depth level
        for i in range(1, recursive_depth + 1):
            points = get_division_points(i)
            marks = create_division_marks(points, i)
            
            # Add nodes and edges to the tree
            nodes = VGroup(root_node)
            edges = VGroup()
            vertical_spacing = 0.5  # Adjust this value as needed for your desired spacing
            add_to_tree(nodes, edges, i, root_x, root_y, initial_space, vertical_spacing, initial_edge_width, initial_node_size)
            tree.add(nodes, edges)

            # Animate division marks and tree nodes and edges simultaneously
            animations = [Create(mark) for mark in marks] + [Create(node) for node in nodes] + [Create(edge) for edge in edges]
            self.play(*animations, run_time=animation_speed)

            self.wait(1)  # Consistent wait time between levels

        self.wait(5)