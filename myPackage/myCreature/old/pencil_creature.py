#!/usr/bin/env python
# sys.path.insert(1, "/Users/axel/Agensit/manim/manim_3b1b")
from manimlib.imports import *

CREATURE_DIR = "/Users/axel/Agensit/manim/manim_3b1b/manimlib/creature/assets/pencil_creatures"


BODY_INDEX = 0
BCKGRD_BODY_INDEX = 8
SPITE_INDEX = 9 
LEFT_EYEBROW_INDEX = 2
RIGHT_EYEBROW_INDEX = 3
LEFT_ARM_INDEX = 4 
RIGHT_ARM_INDEX = 5
LEFT_CIRCLE = 6
MIDDLE_CIRCLE = 7 
RIGHT_CIRCLE = 10
LEFT_EYE_INDEX = 11 
RIGHT_EYE_INDEX = 12
LEFT_PUPIL_INDEX = 13
RIGHT_PUPIL_INDEX = 14
MOUTH_INDEX = 15



class PencilCreature(SVGMobject):
    CONFIG = {
        "color":BLUE_E,
        "background_color": "#e5d4c3",
        "svg_image_dir": "/Users/axel/Agensit/manim/manim_3b1b/manimlib/creature/assets/pencil_creatures",
        "file_name": "pencil",
        "mode": "ask",
        "start_corner": None,
        "flip_at_start": False,
        "stroke_width": 0,
        "stroke_color": BLACK,
        "fill_opacity": 1.0,
        "height": 3,
        "corner_scale_factor": 0.75,
        "pupil_to_eye_width_ratio": 0.4,
        "pupil_dot_to_pupil_width_ratio": 0.3,
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.file_name = f"{self.file_name}_{self.mode}.svg"
        svg_file = os.path.join(self.svg_image_dir, self.file_name)
        SVGMobject.__init__(self, file_name=svg_file, **kwargs)

        if self.flip_at_start:
            self.flip()
        if self.start_corner is not None:
            self.to_corner(self.start_corner)

    def name_parts(self):
        # body
        self.body = VGroup(*[
            self.submobjects[BODY_INDEX],
            self.submobjects[SPITE_INDEX],
        ])
        self.spite = self.submobjects[SPITE_INDEX]
        self.background_body = VGroup(*[
            self.submobjects[LEFT_CIRCLE],
            self.submobjects[MIDDLE_CIRCLE],
            self.submobjects[RIGHT_CIRCLE],
            self.submobjects[BCKGRD_BODY_INDEX]
        ])
        # arms
        self.arms = VGroup(*[
            self.submobjects[LEFT_ARM_INDEX], 
            self.submobjects[RIGHT_ARM_INDEX]
        ])
        # mouth
        self.mouth = self.submobjects[MOUTH_INDEX]
        # eyes and around
        self.eyebrow = VGroup(*[
            self.submobjects[LEFT_EYEBROW_INDEX],
            self.submobjects[RIGHT_EYEBROW_INDEX]
        ])
        self.pupils = VGroup(*[
            self.submobjects[LEFT_PUPIL_INDEX],
            self.submobjects[RIGHT_PUPIL_INDEX]
        ])
        self.eyes = VGroup(*[
            self.submobjects[LEFT_EYE_INDEX],
            self.submobjects[RIGHT_EYE_INDEX]
        ])
        self.eye_parts = VGroup(self.eyes, self.pupils)
       
    def init_colors(self):
        SVGMobject.init_colors(self)
        self.name_parts()

        self.body.set_fill(self.color, opacity=1)
        self.background_body.set_fill(self.background_color, opacity=1)
        self.arms.set_fill(opacity=0)
        self.arms.set_stroke(color=WHITE, opacity=1, width=2)

        self.mouth.set_fill(BLACK, opacity=1)

        self.eyes.set_fill(WHITE, opacity=1)
        self.eyebrow.set_fill(opacity=0)
        self.eyebrow.set_stroke(color=WHITE, opacity=1, width=2)
        self.init_pupils()

        
        return self

    def init_pupils(self):
        # Instead of what is drawn, make new circles.
        # This is mostly because the paths associated
        # with the eyes in all the drawings got slightly
        # messed up.
        for eye, pupil in zip(self.eyes, self.pupils):
            pupil_r = eye.get_width() / 2
            pupil_r *= self.pupil_to_eye_width_ratio
            dot_r = pupil_r
            dot_r *= self.pupil_dot_to_pupil_width_ratio

            new_pupil = Circle(
                radius=pupil_r,
                color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            dot = Circle(
                radius=dot_r,
                color=WHITE,
                fill_opacity=1,
                stroke_width=0,
            )
            new_pupil.move_to(pupil)
            pupil.become(new_pupil)
            dot.shift(
                new_pupil.get_boundary_point(UL) -
                dot.get_boundary_point(UL)
            )
            pupil.add(dot)

    def copy(self):
        copy_mobject = SVGMobject.copy(self)
        copy_mobject.name_parts()
        return copy_mobject
   
    def set_color(self, color):
        self.body.set_fill(color)
        self.color = color
        return self 

    def change_mode(self, mode):
        new_self = self.__class__(
            mode=mode,
        )
        new_self.match_style(self)
        new_self.match_height(self)
        if self.is_flipped() != new_self.is_flipped():
            new_self.flip()
        new_self.shift(self.eyes.get_center() - new_self.eyes.get_center())
        if hasattr(self, "purposeful_looking_direction"):
            new_self.look(self.purposeful_looking_direction)
        self.become(new_self)
        self.mode = mode
        return self

    def get_mode(self):
        return self.mode
    
    def look(self, direction):
        norm = get_norm(direction)
        if norm == 0:
            return
        direction /= norm
        self.purposeful_looking_direction = direction
        for pupil, eye in zip(self.pupils.split(), self.eyes.split()):
            c = eye.get_center()
            right = eye.get_right() - c
            up = eye.get_top() - c
            vect = direction[0] * right + direction[1] * up
            v_norm = get_norm(vect)
            p_radius = 0.5 * pupil.get_width()
            vect *= (v_norm - 0.75 * p_radius) / v_norm
            pupil.move_to(c + vect)
        self.pupils[1].align_to(self.pupils[0], DOWN)
        return self

    def look_at(self, point_or_mobject):
        if isinstance(point_or_mobject, Mobject):
            point = point_or_mobject.get_center()
        else:
            point = point_or_mobject
        self.look(point - self.eyes.get_center())
        return self

    def change(self, new_mode, look_at_arg=None):
        self.change_mode(new_mode)
        if look_at_arg is not None:
            self.look_at(look_at_arg)
        return self

    def get_looking_direction(self):
        vect = self.pupils.get_center() - self.eyes.get_center()
        return normalize(vect)

    def get_look_at_spot(self):
        return self.eyes.get_center() + self.get_looking_direction()

    def is_flipped(self):
        return self.eyes.submobjects[0].get_center()[0] > \
            self.eyes.submobjects[1].get_center()[0]

    def blink(self):
        eye_parts = self.eye_parts
        eye_bottom_y = eye_parts.get_bottom()[1]
        eye_parts.apply_function(
            lambda p: [p[0], eye_bottom_y, p[2]]
        )
        return self
    
    def look_at_u(self):
        for eye, pupil in zip(self.eyes, self.pupils):
            pupil.move_to(eye.get_center())

    def to_corner(self, vect=None, **kwargs):
        if vect is not None:
            SVGMobject.to_corner(self, vect, **kwargs)
        else:
            self.scale(self.corner_scale_factor)
            self.to_corner(DOWN + LEFT, **kwargs)
        return self
    
    def get_bubble(self, *content, **kwargs):
        bubble_class = kwargs.get("bubble_class", ThoughtBubble)
        bubble = bubble_class(**kwargs)
        if len(content) > 0:
            if isinstance(content[0], str):
                content_mob = TextMobject(*content)
            else:
                content_mob = content[0]
            bubble.add_content(content_mob)
            if "height" not in kwargs and "width" not in kwargs:
                bubble.resize_to_content()
        bubble.pin_to(self)
        self.bubble = bubble
        return bubble

    def make_eye_contact(self, pi_creature):
        self.look_at(pi_creature.eyes)
        pi_creature.look_at(self.eyes)
        return self

    def get_all_creature_modes():
        result = []
        prefix = "{}_".format(PencilCreature.CONFIG["file_name"])
        suffix = ".svg"
        for file in os.listdir(CREATURE_DIR):
            if file.startswith(prefix) and file.endswith(suffix):
                result.append(
                    file[len(prefix):-len(suffix)]
                )
        return result

# TODO understand it in Pi creature
def shrug(self):
    pass
# TODO understand it in Pi creature
def get_arm_copies(self):
    pass
class Alex(PencilCreature):
    pass # Nothing else than an alternative name

class Teacher(PencilCreature):
    CONFIG = {
        "color": GREY_BROWN,
        "flip_at_start": True
    }

 
