from manim import *

class DenseSetVisualization(MovingCameraScene):
    def construct(self):
        # Define the endpoints and the points between them
        left_point = Dot([-4, 0, 0], color=WHITE).scale(1.5)
        right_point = Dot([4, 0, 0], color=WHITE).scale(1.5)
        middle_points = VGroup(*[Dot([x, 0, 0], color=WHITE).scale(0.5) for x in np.linspace(-3.5, 3.5, 20)])

        # Group all points together
        all_points = VGroup(left_point, right_point, middle_points)

        # Add all points to the scene
        self.add(all_points)

        # Save the state of the camera
        self.camera.frame.save_state()

        # Focus on two of the middle points
        zoomed_points = VGroup(middle_points[9], middle_points[10])
        self.play(self.camera.frame.animate.set(width=zoomed_points.width * 0.1).move_to(zoomed_points.get_center()))

        self.wait()

        # Restore the camera to the original state
        self.play(Restore(self.camera.frame))

        # Clear the screen and reset for the next loop
        self.remove(all_points)

        # Recreate the initial scene to start the looping process again
        self.add(left_point, right_point, middle_points)

        # The scene will start over from this point, creating the illusion of infinite zooming
        self.wait()