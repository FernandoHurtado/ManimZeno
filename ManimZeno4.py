from manim import *

class ManimZeno4(MovingCameraScene):
    def construct(self):

        subtitle = Title("The Dichotomy Procedure")
        self.add(subtitle)


        n_line = NumberLine(x_range=[0,1], length=10, include_numbers=True,)
        self.play(Create(n_line))


        tracker = ValueTracker(0)
        def get_line_obj():
            sp = n_line.number_to_point(tracker.get_value())
            ep = sp + UP*1.5
            arrow = Arrow(ep,sp,buff=0,color=RED)
            num = DecimalNumber(tracker.get_value(), color=RED, num_decimal_places=3,)
            num.next_to(arrow, UP)
            return VGroup(arrow, num)
        obj = always_redraw(get_line_obj)
        self.add(obj)
     
        runner = 0
        sw = 10.0

        self.wait(2)

        for runner_step in range(1,12,1):
            runner = runner + 1/2**runner_step
            self.play(tracker.animate.set_value(runner),run_time=2,)
            
            self.wait(1)
            sw = sw - 1

            sp = n_line.number_to_point(tracker.get_value())
            ep = sp + DOWN*1.5
            newarrow = Arrow(ep,sp,buff=0,color=YELLOW, max_tip_length_to_length_ratio=0.0, stroke_width= sw,)
            self.add(newarrow) 

        sp = n_line.number_to_point(tracker.get_value())
        ep = sp + DOWN*1.5
        finalarrow = Arrow(ep,sp,buff=0,color=YELLOW, max_tip_length_to_length_ratio=0.0, stroke_width= 0.5,)
        self.add(finalarrow) 

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.set(width=3).move_to(newarrow))

        self.wait(1)

        self.play(self.camera.frame.animate.set(width=0.3).move_to(newarrow))


        self.wait(5)
