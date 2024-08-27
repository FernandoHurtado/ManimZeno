from manim import *

class MultiDots(VGroup):
  def __init__(self, d_left:Dot, d_right:Dot, n=5, scale=0.5, **kwargs):
    super().__init__()
    l = Line(d_left.get_center(), d_right.get_right())

    dots = VGroup(*[
      Dot(l.point_from_proportion(i / n), **kwargs).set(width=d_left.width * scale)
      for i in range(n)
    ])
    dots.move_to(l.get_center())
    self.add(*dots)

class ManimMeasureTree2(MovingCameraScene):
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

        # Function to create division marks with decreasing size 
        def create_division_marks(points, depth):
            marks = []
            length_factor = max(0.2, 3 - (depth * 0.5))
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
                add_to_tree(nodes, edges, depth - 1, left_x, new_y, space / 2, vertical_spacing, edge_width * 0.95, node_size * 0.85    )
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
            vertical_spacing = 0.525  # Adjust this value as needed for your desired spacing
            add_to_tree(nodes, edges, i, root_x, root_y, initial_space, vertical_spacing, initial_edge_width, initial_node_size)
            tree.add(nodes, edges)

            # Animate division marks and tree nodes and edges simultaneously
            animations = [Create(mark) for mark in marks] + [Create(node) for node in nodes] + [Create(edge) for edge in edges]

            # Add step number and the number of parts at each step
            step_number = MathTex(f"{i}", color=WHITE).scale(0.7)
            parts_number = MathTex(r"2^{" + f"{i}" + r"}", color=WHITE).scale(0.7)
            
            # Position step number and parts number to the left of the binary tree, at different horizontal positions
            step_number.move_to(np.array([-6.5, root_y - (i - 1) * vertical_spacing - 0.5, 0]))
            parts_number.move_to(np.array([-6, root_y - (i - 1) * vertical_spacing - 0.5, 0]))  # Align with step_number

            # Include step number and parts number in the animations
            animations.extend([Write(step_number), Write(parts_number)])
            
            # Add fractions above each division mark, avoiding overlaps and making them smaller progressively
            if i <= 6:  # Only display fractions up to step 6
                # Calculate the size for fractions based on the current depth
                fraction_size = max(0.15, 0.5 - 0.05 * i)  # Start smaller and decrease slightly with each step
                for j in range(1, 2**i, 2):  # Place fractions only at the midpoint of each interval
                    fraction = MathTex(r"\frac{1}{" + str(2**i) + r"}", color=WHITE).scale(fraction_size)
                    # Position the fraction above the midpoint of the interval
                    fraction.move_to(n_line.number_to_point(j / 2**i) + DOWN * 1 - i * vertical_spacing * UP)
                    animations.append(Write(fraction)) 
                    
            self.play(*animations, run_time=animation_speed)

            self.wait(1)  # Consistent wait time between levels

        # Create the set representation with large brackets
        set_width = 10  # Width of the set representation
        set_bracket_left = MathTex(r"\{").scale(2)  # Correct the brackets for sets
        set_bracket_right = MathTex(r"\}").scale(2)
        center_point = n_line.get_center()  # Current center point of the number line
        set_bracket_left.move_to(center_point + DOWN*6 + LEFT*(set_width/2))
        set_bracket_right.move_to(center_point + DOWN*6 + RIGHT*(set_width/2))

        # Create the omega symbol and the "2^ℕ" notation
        omega_symbol = MathTex(r"\omega").scale(0.7)
        two_to_the_n_symbol = MathTex(r"2^{\mathbb{N}}").scale(0.7)

        # Position the omega symbol and the "2^ℕ" notation at the specified horizontal locations
        # and align them vertically with the set brackets which are at DOWN*3
        omega_symbol.move_to(np.array([-6.5, set_bracket_left.get_y(), 0]))
        two_to_the_n_symbol.move_to(np.array([-6, set_bracket_right.get_y(), 0]))

        # Create the ellipsis that indicates the continuation of the process below the binary tree
        continuation_dots = MathTex(r"\cdots").next_to(tree, DOWN, buff=0.5)

        # Create the continuation dots that will appear below the step number and part numbers
        left_continuation_dots = MathTex(r"\cdots")
        continuation_dots_y = continuation_dots.get_center()[1]
        left_continuation_dots.move_to(np.array([-6.25, continuation_dots_y, 0]))  # Centered between -6 and -6.5
        
        # Animate the creation of the continuation dots
        self.play(Write(continuation_dots), Write(left_continuation_dots))

        # Animate the creation of set brackets and symbols
        self.play(Write(set_bracket_left), Write(set_bracket_right),
                  Write(omega_symbol), Write(two_to_the_n_symbol))

        ## CODE FOR THE DENSE SET
        camera = self.camera.frame
        camera.save_state()

        d1 = Dot().scale(3)
        d2 = Dot().scale(3)

        d1.move_to(center_point + DOWN*6 + LEFT*(set_width/2))
        d2.move_to(center_point + DOWN*6 + RIGHT*(set_width/2))

        def get_dist_between_dots(d1, d2):
          return np.linalg.norm(d1.get_center() - d2.get_center())

        dist_dots = get_dist_between_dots(d1, d2)

        prop1 = d1.width  / camera.width
        prop2 = dist_dots / camera.width

        mp1 = MultiDots(d1, d2, n=100, scale=0.04)

        nd1, nd2 = ndots = mp1[4:6]
        ndist = get_dist_between_dots(nd1, nd2)
        ncamera_width = ndist / prop2
        ndot_width    = prop1 * ncamera_width

        self.add(d1.fade(1), d2.fade(1), mp1)
        self.play(
          camera.animate.move_to(ndots).set(width=ncamera_width),
          nd1.animate.set(width=ndot_width),
          nd2.animate.set(width=ndot_width),
          run_time=3
        )
        
        d1 = nd1
        d2 = nd2

        def get_dist_between_dots(d1, d2):
          return np.linalg.norm(d1.get_center() - d2.get_center())

        dist_dots = get_dist_between_dots(d1, d2)

        prop1 = d1.width  / camera.width
        prop2 = dist_dots / camera.width

        mp1 = MultiDots(d1, d2, n=100, scale=0.04)

        nd1, nd2 = ndots = mp1[4:6]
        ndist = get_dist_between_dots(nd1, nd2)
        ncamera_width = ndist / prop2
        ndot_width    = prop1 * ncamera_width

        self.add(d1, d2, mp1)
        self.play(
          camera.animate.move_to(ndots).set(width=ncamera_width),
          nd1.animate.set(width=ndot_width),
          nd2.animate.set(width=ndot_width),
          run_time=3
        )
        
                
        d1 = nd1
        d2 = nd2

        def get_dist_between_dots(d1, d2):
          return np.linalg.norm(d1.get_center() - d2.get_center())

        dist_dots = get_dist_between_dots(d1, d2)

        prop1 = d1.width  / camera.width
        prop2 = dist_dots / camera.width

        mp1 = MultiDots(d1, d2, n=100, scale=0.04)
        
        nd1, nd2 = ndots = mp1[4:6]

        self.add(mp1)
        self.wait(10)
        
        # Zoom out to the initial camera state
        self.play(Restore(camera), run_time=3)
        self.wait()


        

        # Hold the final scene
        self.wait(5)
        
"""
        

        def number_to_index(self, number, total_points):
            # Convert a number on the number line to the corresponding index in the dense set
            return min(int(number * total_points), total_points - 1)

        # New code for runner's traversal with circles and lines
        tracker = ValueTracker(0)

        def get_line_obj():
            sp = n_line.number_to_point(tracker.get_value())
            ep = sp + UP*0.5
            arrow = Arrow(ep, sp, buff=0, color=BLUE)
            num = DecimalNumber(tracker.get_value(), color=BLUE, num_decimal_places=3)
            num.next_to(arrow, UP)
            return VGroup(arrow, num)

        line_obj = always_redraw(get_line_obj)
        self.add(line_obj)

        runner = 0
        sw = 10.0
        vertical_spacing = 0.525  # Spacing between steps

        self.wait(2)

        circle_positions = []  # List to store positions of circles

        for runner_step in range(1, 12, 1):
            runner = runner + 1/2**runner_step
            self.play(tracker.animate.set_value(runner), run_time=2)
            self.wait(1)
            sw = sw - 1

            sp = n_line.number_to_point(tracker.get_value())
            ep = sp + DOWN*(1 + vertical_spacing * (runner_step - 1))
            newarrow = Arrow(ep, sp, buff=0, color=BLUE, max_tip_length_to_length_ratio=0.0, stroke_width=sw)
            self.add(newarrow)

            # Drawing a circle at the endpoint of the arrow
            circle = Circle(radius=0.1, color=BLUE).move_to(ep)
            self.add(circle)
            circle_positions.append(ep)

            # Drawing a line connecting this circle to the previous circle
            if len(circle_positions) > 1:
                connecting_line = Line(start=circle_positions[-2], end=circle_positions[-1], color=BLUE, stroke_width=5)
                self.add(connecting_line)

        self.wait(10)
        
        """
