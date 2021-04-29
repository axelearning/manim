from manim.constants import *
from manim.mobject.svg.svg_mobject import SVGMobject, VGroup, VMobject
from manim.mobject.mobject import Mobject
from manim.utils.color import *
from manim.mobject.svg.tex_mobject import Tex

from pathlib import Path

SVG_DIR = Path(__file__).parent / "assets/"

BACKGROUND_COLOR = '#0f0f0f' #DARK-GREY
BACKGROUND_OPACITY = 1
STROKE_COLOR = WHITE
STROKE_WIDTH = 3
POSITION_FACTOR = 1.1 

class Bubble(SVGMobject):

        def __init__(
            self,
            bubble_mode = "speech", 
            direction = LEFT, 
            height = 5,
            width = 8,
            **kwargs
        ):
            file_name = str(SVG_DIR / f"bubble_{bubble_mode}.svg")
            SVGMobject.__init__(
                self, 
                file_name=file_name,
                **kwargs
            )

            self.stretch_to_fit_height(height)
            self.stretch_to_fit_width(width)

            self.direction = direction
            if self.direction[0] < 0:
                    self.flip()

            self.content = Mobject()

        def init_colors(self, propagate_colors=True):
            self.set_fill(color=BACKGROUND_COLOR, opacity=BACKGROUND_OPACITY)
            self.set_stroke(color=STROKE_COLOR, width=STROKE_WIDTH)

        def get_tip(self):
            return self.get_boundary_point(DOWN)


        def get_bubble_center(self):
            bubble_center_adjustment_factor = 1/8
            return self.get_center() + bubble_center_adjustment_factor * self.get_height() * UP


        def move_tip_to(self, point):
            mover = VGroup(self)
            if self.content:
                mover.add(self.content)
            mover.shift(point - self.get_tip())
            return self


        def flip(self, axis=UP):
            Mobject.flip(self, axis=axis)
            if abs(axis[1]) > 0:
                self.direction = -np.array(self.direction)
            return self


        def pin_to(self, mobject):
            mob_center = mobject.get_center()
            want_to_flip = np.sign(mob_center[0]) != np.sign(self.direction[0])
            if want_to_flip:
                self.flip()

            boundary_point = mobject.get_critical_point(UP - self.direction)
            self.move_tip_to(boundary_point)
            return self


        def write(self, *text):
            self.add_content(Tex(*text))
            return self


        def add_content(self, mobject):
            self.position_mobject_inside(mobject)
            self.content = mobject
            return self.content


        def position_mobject_inside(self, mobject):
            content_scale_factor = 0.75
            scaled_width = content_scale_factor * self.get_width()
            if mobject.get_width() > scaled_width:
                mobject.set_width(scaled_width)
            mobject.shift(self.get_bubble_center() - mobject.get_center())
            return mobject


        def resize_to_content(self):
            target_width = self.content.get_width()
            target_width += max(MED_LARGE_BUFF, 2) 
            target_height = self.content.get_height()
            target_height += 2.5* LARGE_BUFF 
            tip_point = self.get_tip()
            self.stretch_to_fit_width(target_width)
            self.stretch_to_fit_height(target_height)
            self.move_tip_to(tip_point)
            self.position_mobject_inside(self.content)


        def clear(self):
            self.add_content(VMobject())
            return self

