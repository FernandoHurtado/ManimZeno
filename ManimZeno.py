from manim import *

class ManimZeno1(Scene):
    def construct(self):

        title = Tex('Have we solved Zeno\'s Paradoxes?').scale(1.4)     
        self.play(Create(title, run_time=3))  

        self.wait(20)

        subtitle = Title("Have we solved Zeno's Paradoxes?")
        self.play(Transform(title,subtitle))

        blist1 = BulletedList("Aristotle and the Runner Paradox","Parmenides' notion of continuum","The Dichotomy procedure","The Cardinal Problem","The Mereological Problem")

        #blist1 = BulletedList("Item 1", "Item 2", "Item 3", height=2, width=2)
        

        self.play(Write(blist1, run_time=4))

        self.wait(20)

        self.play(FadeOut(blist1,title,subtitle))        

        subtitle1 = Title("1. Aristotle and the Runner Paradox")
        self.play(Create(subtitle1))

        self.wait(3)
        
        ##FORMATO PARA CITAS
        
        quote1 = Tex("Again, if length and time could thus be composed of indivisibles, they could be divided into indivisibles, since each is divisible into the parts of which it is composed. But, as we saw, no continuous thing is divisible into things without parts. Nor can there be anything of any other kind intermediate between the parts or between the moments: for if there could be any such thing it is clear that it must be either indivisible or divisible, and if it is divisible, it must be divisible either into indivisibles or into divisibles that are infinitely divisible, in which case it is continuous.").scale(0.75)
        author1 = Tex("Aristotle, Physics Book VI").scale(0.5)

        author1.next_to(quote1.get_corner(DOWN),DOWN)
        self.add(quote1)
        self.play(Create(author1))

        self.wait(10)

        self.play(FadeOut(quote1,author1))

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
        
        self.wait(2)

        for runner_step in range(1,6,1):
            runner = runner + 1/2**runner_step
            self.play(tracker.animate.set_value(runner),run_time=2,)

            self.wait(2)
 
        #this is normally associated with the modern notion of limit

        dichotomysum = MathTex(r'\sum_{n=1}^{\infty}(\frac{1}{2^n})').scale(0.85)
        dichotomysum.next_to(n_line, DOWN*1.5)
        self.play(Create(dichotomysum))

        self.wait(5)

        dichotomysumresult = MathTex(r'= 1').scale(0.85)
        dichotomysumresult.next_to(dichotomysum, RIGHT)
        self.play(Create(dichotomysumresult))

        self.wait(5)

        self.play(FadeOut(n_line, obj, dichotomysum, dichotomysumresult))
        

        self.wait(1)

        ##FORMATO PARA CITAS
        
        quote2 = Tex("[...]the dichotomy argument, which assumes indivisible magnitudes.").scale(0.75)
        author2 = Tex("Aristotle, Physics Book I").scale(0.5)

        author2.next_to(quote2.get_corner(DOWN),DOWN)
        self.add(quote2)
        self.play(Create(author2))

        self.wait(10)

        self.play(FadeOut(subtitle1, quote2,author2))

        
        #subtitle2 = Title("Parmenides' notion of Continuity")
        #self.play(Create(subtitle2))
        #subtitle3 = Title("The Dichotomy procedure")
        #subtitle4 = Title("The Cardinal Problem")
        #subtitle5 = Title("The Mereological Problem")
