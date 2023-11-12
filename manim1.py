from manim import *

class ManimZeno(Scene):
    def construct(self):

        text1 = Tex('Have we solved Zeno\'s Paradoxes?').scale(1.4)     
        self.play(Create(text1))  
        self.wait(3)
        self.play(FadeOut(text1))

        n_line = NumberLine(x_range=[0,1,0.1], length=10, include_numbers=True,)
        self.play(Create(n_line))


        tracker = ValueTracker(0)
        def get_line_obj():
            sp = n_line.number_to_point(tracker.get_value())
            ep = sp + UP*1.5
            arrow = Arrow(ep,sp,buff=0,color=RED)
            num = DecimalNumber(tracker.get_value(), color=RED)
            num.next_to(arrow, UP)
            return VGroup(arrow, num)
        obj = always_redraw(get_line_obj)
        self.add(obj)
        
        runner = 0

        for runner_step in range(1,5,1):
            runner = runner + 1/2**runner_step
            self.play(tracker.animate.set_value(runner),run_time=2,)
            self.wait(2)

