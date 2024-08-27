from manim import *
config.disable_caching = True

class MultiDots(VGroup):
    def __init__(self, d_left: Dot, d_right: Dot, n=5, scale=0.5, **kwargs):
        super().__init__()
        l = Line(d_left.get_center(), d_right.get_right())

        dots = VGroup(*[
            Dot(l.point_from_proportion(i / n), **kwargs).set(width=d_left.width * scale)
            for i in range(n)
        ])
        dots.move_to(l.get_center())
        self.add(*dots)


class DenseSetVisualization(MovingCameraScene):
    def construct(self):
        camera = self.camera.frame
        camera.save_state()

        d1 = Dot().scale(3)
        d2 = Dot().scale(3)

        d1.to_edge(LEFT)
        d2.to_edge(RIGHT)

        def get_dist_between_dots(d1, d2):
            return np.linalg.norm(d1.get_center() - d2.get_center())

        for _ in range(5):
            dist_dots = get_dist_between_dots(d1, d2)

            prop1 = d1.width / camera.width
            prop2 = dist_dots / camera.width

            mp1 = MultiDots(d1, d2, n=100, scale=0.1)

            nd1, nd2 = ndots = mp1[4:6]
            nd1.set_color(BLUE)
            nd2.set_color(BLUE)
            
            ndist = get_dist_between_dots(nd1, nd2)
            ncamera_width = ndist / prop2
            ndot_width = prop1 * ncamera_width

            # New MultiDots for the next zoom
            new_mp1 = MultiDots(nd1, nd2, n=100, scale=0.1)
            new_mp1.set_opacity(0)  # Initially invisible

            self.add(d1, d2, mp1, new_mp1)
            self.play(
                camera.animate.move_to(ndots).set(width=ncamera_width),
                nd1.animate.set(width=ndot_width),
                nd2.animate.set(width=ndot_width),
                FadeIn(new_mp1, run_time=3),
                run_time=3
            )
            self.wait()

            # Update d1 and d2 for the next iteration
            d1, d2 = nd1, nd2
            mp1 = new_mp1

        # Zoom out to the initial camera state
        self.play(Restore(camera), run_time=3)
        self.wait()



