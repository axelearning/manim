from manim import *

from myPackage.myCreature.pencil import PencilCreature
from myPackage.myCreature.pencil_animations import (
    Asks, Blink, Appears, DisAppears, BubbleIntroduction, RemoveBubble, Says, Thinks)
from myPackage.myCreature.pencil_creature_scene import TeacherStudentsScene
from myPackage.myCreature.bubble import Bubble

class SceneTest(Scene):
    def construct(self):
        formula = Tex("f(x) = ax + by + c")
        circle = Circle(fill_color=RED).next_to(formula, direction=DOWN)
        self.add(formula, circle)

        on_screen = VGroup(*self.mobjects)
        border = SurroundingRectangle(on_screen, buff=1)
        self.play(Create(border))
        # self.camera
        
        # self.play(on_screen.animate.scale(1/3).to_corner(UL))


