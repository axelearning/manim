import itertools as it
import random

from manim.constants import *
from manim.utils.color import *

from manim.animation.composition import LaggedStart
from manim.mobject.mobject import Group, Mobject
from manim.mobject.frame import ScreenRectangle
from manim.mobject.types.vectorized_mobject import VGroup
from manim.scene.scene import Scene
from manim.utils.rate_functions import squish_rate_func, there_and_back
from manim.utils.space_ops import get_norm
from manim.animation.composition import AnimationGroup
from manim.animation.fading import FadeInFrom
from manim.animation.transform import (
    ReplacementTransform, ApplyMethod, Transform, MoveToTarget, ApplyFunction
)

from .pencil import PencilCreature, Alex
# from .bubble import Bubble
from .pencil_animations import (
    Blink, Appears, DisAppears, BubbleIntroduction, RemoveBubble
)


SCALE_FACTOR = 1.6


class CreatureScene(Scene):

    def setup(
        self,
        creatures_start_on_screen = True,
        default_creature_start_corner = DR,
        default_creature_kwargs= {
            "color": GREY_BROWN,
            "flip_at_start": True,
        },
        total_wait_time  = 0,
        seconds_to_blink  = 3,
    ):
        self.creatures_start_on_screen = creatures_start_on_screen
        self.default_creature_start_corner = default_creature_start_corner
        self.default_creature_kwargs = default_creature_kwargs
        self.total_wait_time = total_wait_time
        self.seconds_to_blink = seconds_to_blink

        self.creatures = VGroup(*self.create_creatures())
        self.creature = self.get_primary_creature()
        if self.creatures_start_on_screen:
            self.add(*self.creatures)

    def create_creatures(self):
        """
        Likely updated for subclasses
        """
        return VGroup(self.create_creature())

    def create_creature(self):
        creature = PencilCreature(**self.default_creature_kwargs).scale(SCALE_FACTOR)
        creature.to_corner(self.default_creature_start_corner)
        return creature
    
    def get_creatures(self):
        return self.creatures
    
    def get_primary_creature(self):
        return self.creatures[0]

    def any_creatures_on_screen(self):
        return len(self.get_on_screen_creatures()) > 0

    def get_on_screen_creatures(self):
        mobjects = self.get_mobject_family_members()
        return VGroup(*[
            pencil for pencil in self.get_creatures()
            if pencil in mobjects
        ])

    def has_bubble(self, pencil):
        # on_screen_mobjects = self.camera.extract_mobject_family_members(self.get_mobjects())
        on_screen_mobjects = self.get_mobject_family_members()
        return hasattr(pencil, "bubble") and \
            pencil.bubble is not None and \
            pencil.bubble in on_screen_mobjects
        
    def introduce_bubble(self, content, creature=None, **kwargs):
        if not creature:
            creature = self.get_primary_creature()

        keep_other_bubble = kwargs.pop("keep_other_bubble", False)
        bubble_class = kwargs.pop("bubble_mode", "speech")
        target_mode = kwargs.pop(
            "target_mode",
            "think" if bubble_class == "thought" else "ask"
        )
        bubble_kwargs = kwargs.pop("bubble_kwargs", {})
        bubble_removal_kwargs = kwargs.pop("bubble_removal_kwargs", {})
        added_anims = kwargs.pop("added_anims", [])

        anims = []
        creatures_with_bubbles = list(filter(self.has_bubble, self.get_creatures()))
        # Remove other bubble from different creature
        if not keep_other_bubble:
            anims += [
                RemoveBubble(pencil, **bubble_removal_kwargs)
                for pencil in creatures_with_bubbles 
                if creature not in creatures_with_bubbles
            ]
        # if the creature as already a bubble
        if creature in creatures_with_bubbles:
            creatures_with_bubbles.remove(creature)
            old_bubble = creature.bubble
            bubble = creature.get_bubble(
                content,
                bubble_mode=bubble_class,
                **bubble_kwargs
            )
            anims += [
                ReplacementTransform(old_bubble, bubble),
                ReplacementTransform(old_bubble.content, bubble.content),
                creature.change_mode, target_mode
            ]
        else:
            anims.append(BubbleIntroduction(
                creature,
                content,
                bubble_mode=bubble_class,
                bubble_kwargs=bubble_kwargs,
                target_mode=target_mode,
                **kwargs
            ))
        anims += added_anims

        self.play(*anims, **kwargs)

    def creature_says(self, content, **kwargs):
        self.introduce_bubble(
            content,
            bubble_mode="speech",
            target_mode="confident",
            **kwargs
        )
    
    def creature_thinks(self, content, **kwargs):
        self.introduce_bubble(
            content,
            bubble_mode="thought",
            target_mode="think",
            **kwargs
        )

    def say(self, content, **kwargs):
        self.creature_says(content, **kwargs)
    
    def think(self, content, **kwargs):
        self.creature_thinks(content, **kwargs)

    def clear_bubble(self, **kwargs):
        creatures_with_bubbles = list(filter(self.has_bubble, self.get_creatures()))
        anims = []
        for creature in creatures_with_bubbles:
            anims.append(RemoveBubble(creature))
            creature.bubble = None
        if anims:
            self.play(*anims, **kwargs)
            
    def compile_play_args_to_animation_list(self, *args, **kwargs):
        """
        Add animations so that all creatures look at the
        first mobject being animated with each .play call
        """
        animations = Scene.compile_play_args_to_animation_list(self, *args, **kwargs)
        anim_mobjects = Group(*[a.mobject for a in animations])
        all_movers = anim_mobjects.get_family()
        if not self.any_creatures_on_screen():
            return animations

        creatures = self.get_on_screen_creatures()
        non_creature_anims = [
            anim
            for anim in animations
            if len(set(anim.mobject.get_family()).intersection(creatures)) == 0
        ]
        if len(non_creature_anims) == 0:
            return animations
        first_anim = non_creature_anims[0]
        main_mobject = first_anim.mobject
        for creature in creatures:
            if creature not in all_movers:
                animations.append(ApplyMethod(
                    creature.look_at,
                    main_mobject,
                ))
        return animations

    def blink(self):
        self.play(Blink(random.choice(self.get_on_screen_creatures())))

    def joint_blink(self, creatures=None, shuffle=True, **kwargs):
            if creatures is None:
                creatures = self.get_on_screen_creatures()
            creatures_list = list(creatures)
            if shuffle:
                random.shuffle(creatures_list)

            def get_rate_func(pencil):
                index = creatures_list.index(pencil)
                proportion = float(index) / len(creatures_list)
                start_time = 0.8 * proportion
                return squish_rate_func(
                    there_and_back,
                    start_time, start_time + 0.2
                )

            self.play(*[
                Blink(pencil, rate_func=get_rate_func(pencil), **kwargs)
                for pencil in creatures_list
            ])
            return self

    def wait(self, time=1, blink=True, **kwargs):
        if "stop_condition" in kwargs:
            self.non_blink_wait(time, **kwargs)
            return
        while time >= 1:
            time_to_blink = self.total_wait_time % self.seconds_to_blink == 0
            if blink and self.any_creatures_on_screen() and time_to_blink:
                self.blink()
            else:
                self.non_blink_wait(**kwargs)
            time -= 1
            self.total_wait_time += 1
        if time > 0:
            self.non_blink_wait(time, **kwargs)
        return self
    
    def non_blink_wait(self, time=1, **kwargs):
        Scene.wait(self, time, **kwargs)
        return self
    
    def change_mode(self, mode, run_time=0.5):
        self.play(self.get_primary_creature().animate.change_mode(mode), run_time=run_time)

    def look_at(self, thing_to_look_at, creatures=None, **kwargs):
        if creatures is None:
            creatures = self.get_creatures()
        args = list(it.chain(*[
            [pencil.look_at, thing_to_look_at]
            for pencil in creatures
        ]))
        self.play(*args, **kwargs)

    def appears(self, creatures=[], **kwargs):
        if not creatures:
            creatures = self.creature

        if isinstance(creatures, PencilCreature):
            self.play(Appears(creatures, **kwargs))
        else:
            self.play(*[Appears(creature, **kwargs) for creature in creatures])  

    def disappears(self, creature=None, **kwargs):
        anims = []
        if not creature:
            creature = self.creature
        if creature.bubble:
            anims = [RemoveBubble(creature)]

        anims.append(DisAppears(creature, **kwargs))
        self.play(LaggedStart(*anims, lag_ratio=0.5))

    def look_at_u(self, creature=None, **kwargs):
        if not creature:
            creature = self.creature

        creature.generate_target()
        creature.target.look_at_u()
        self.play(MoveToTarget(creature))

    def show(self, mobject, creature=None, target_mode="confident", added_anims=None, **kwargs):
        if not creature:
            creature = self.creature

        self.hold_up_spot = creature.get_corner(UL) + MED_LARGE_BUFF * UP
        mobject.move_to(self.hold_up_spot, DOWN)
        mobject.shift_onto_screen()
        mobject_copy = mobject.copy()
        mobject_copy.shift(DOWN)
        mobject_copy.fade(1)
        added_anims = added_anims or []
        self.play(
            ReplacementTransform(mobject_copy, mobject),
            creature.animate.change(target_mode),
            *added_anims
        )


class TeacherStudentsScene(CreatureScene):

    def setup(
        self,
        student_colors = [BLUE_D, BLUE_E, BLUE_D],
        teacher_color = GREY_BROWN,
        student_scale_factor = 0.8,
        screen_height = 3,
    ):
        self.student_colors = student_colors
        self.teacher_color = teacher_color
        self.student_scale_factor = student_scale_factor
        self.screen = ScreenRectangle(height=screen_height).set_fill(BLACK, opacity=1)
        self.screen.to_corner(UL)
        CreatureScene.setup(self)
    
    def create_creatures(self):
        self.teacher = Alex(color=self.teacher_color).scale(SCALE_FACTOR)
        self.teacher.to_corner(DR)
        self.students = VGroup(*[
            Alex(color=c).scale(SCALE_FACTOR)
            for c in self.student_colors
        ])
        self.students.arrange(RIGHT, buff=0.5)
        # self.students.arrange(RIGHT)
        self.students.scale(self.student_scale_factor)
        self.students.to_corner(DL)
        self.teacher.look_at(self.students[-1].eyes)
        for student in self.students:
            student.look_at(self.teacher.eyes)

        return [self.teacher] + list(self.students)

    def get_teacher(self):
        return self.teacher

    def get_students(self):
        return self.students

    def teacher_says(self, content, **kwargs):
        return self.creature_says(content, creature=self.get_teacher(), **kwargs)

    def student_says(self, content, **kwargs):
        student = self.get_students()[kwargs.get("student_index", -1)]
        return self.creature_says(content, creature=student, **kwargs)
    
    def teacher_thinks(self, content, **kwargs):
        return self.creature_thinks(content, creature=self.get_teacher(), **kwargs)
    
    def student_thinks(self, content, **kwargs):
        student = self.get_students()[kwargs.get("student_index", -1)]
        return self.creature_thinks(content, creature=student, **kwargs)

    def change_all_student_modes(self, mode, **kwargs):
        self.change_student_modes(*[mode] * len(self.students), **kwargs)

    def change_student_modes(self, *modes, **kwargs):
        added_anims = kwargs.pop("added_anims", [])
        self.play(self.get_student_changes(*modes, **kwargs), *added_anims)
    
    def get_student_changes(self, *modes, **kwargs):
        pairs = list(zip(self.get_students(), modes))
        pairs = [(s, m) for s, m in pairs if m is not None]
        start = VGroup(*[s for s, m in pairs])
        target = VGroup(*[s.copy().change_mode(m) for s, m in pairs])
        if "look_at_arg" in kwargs:
            for pencil in target:
                pencil.look_at(kwargs["look_at_arg"])
        anims = [
            Transform(s, t)
            for s, t in zip(start, target)
        ]
        return LaggedStart(
            *anims,
            lag_ratio=kwargs.get("lag_ratio", 0.5),
            run_time=1,
        )


    def teacher_holds_up(self, mobject, target_mode="ask", added_anims=None, **kwargs):
        self.hold_up_spot = self.teacher.get_corner(UL) + MED_LARGE_BUFF * UP
        mobject.move_to(self.hold_up_spot, DOWN)
        mobject.shift_onto_screen()
        mobject_copy = mobject.copy()
        mobject_copy.shift(DOWN)
        mobject_copy.fade(1)
        added_anims = added_anims or []
        self.play(
            ReplacementTransform(mobject_copy, mobject),
            self.teacher.animate.change(target_mode),
            *added_anims
        )

    def all_look_at_u(self, **kwargs):
        anims = []
        for creature in self.creatures:
            creature.generate_target()
            creature.target.look_at_u()
            anims.append(MoveToTarget(creature))
        self.play(*anims)


    def zoom_out(self, board=Mobject()):
        def zoom_out(mob):
            mob.scale(1/3)
            mob.to_corner(UL)
            return mob
        self.play(
            LaggedStart(
                ApplyFunction(zoom_out, board),
                AnimationGroup(
                    *[FadeInFrom(student) for student in self.students],
                    FadeInFrom(self.teacher, RIGHT),
                ),
                lag_ratio = 0.1,
                run_time=2
            ),
        )