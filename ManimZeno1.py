from manim import *

class ManimZeno1(Scene):
    def construct(self):

        subtitle1 = Title("Parmenides' notion of continuum")
        self.add(subtitle1)

        self.wait(3)

        n_line = NumberLine(x_range=[0,1], length=10, include_numbers=True,)
        self.play(Create(n_line))
        
        self.wait(10)

        tracker = ValueTracker(0.49901)
        def get_line_obj():
            sp = n_line.number_to_point(tracker.get_value())
            ep = sp + UP*1.5
            arrow = Arrow(ep,sp,buff=0,color=RED)
            num = DecimalNumber(tracker.get_value(), color=RED, num_decimal_places=6,)
            num.next_to(arrow, UP)
            return VGroup(arrow, num)
        obj = always_redraw(get_line_obj)
        self.add(obj)
        
        runner = 0

        self.play(tracker.animate.set_value(0.49999),run_time=30)


