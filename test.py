from manim import *

from myPackage.myCreature.pencil import PencilCreature
from myPackage.myCreature.pencil_animations import Blink, Appears, DisAppears

class Pencil(Scene):
    def construct(self):
        al = PencilCreature()
        self.wait()
        self.play(Appears(al))
        self.wait()
        self.play(DisAppears(al))


        