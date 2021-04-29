from manim import *

from myPackage.myCreature.pencil import PencilCreature
from myPackage.myCreature.pencil_animations import Asks, Blink, Appears, DisAppears, BubbleIntroduction, RemoveBubble, Says, Thinks
from myPackage.myCreature.bubble import Bubble

class BubbleTeste(Scene):
    def construct(self):

        al = PencilCreature(mode='confident')
        al.move_to(3*DOWN+5*LEFT)

        
        self.play(
            Says(al, "Yooo!")
        )
        self.wait()

        self.play(RemoveBubble(al))
        self.wait()
        