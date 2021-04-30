from manim.utils.rate_functions import squish_rate_func, there_and_back, exponential_decay
from manim.animation.transform import ApplyMethod, MoveToTarget
from manim.animation.fading import FadeInFrom, FadeOutAndShift, FadeOut
from manim.animation.composition import AnimationGroup
from manim.animation.creation import Uncreate, Write
from manim.constants import *
from manim.mobject.mobject import Group

from .pencil import PencilCreature


class Blink(ApplyMethod):
    def __init__(self, creature, **kwargs):
        ApplyMethod.__init__(
            self, 
            creature.blink, 
            rate_func = squish_rate_func(there_and_back),
            **kwargs
        )


class Appears(FadeInFrom):
    def __init__(self, mobject, **kwargs):
        assert isinstance(mobject, PencilCreature)
        super().__init__(
            mobject, 
            rate_fct = exponential_decay,
            run_time = 0.5,
            direction = RIGHT,
            **kwargs
        )
        if "target_mode" in kwargs:
            mobject.change(kwargs.get("target_mode"))
        if "look_at" in kwargs:
            mobject.look_at(kwargs.get("look_at"))


class DisAppears(FadeOutAndShift):
    def __init__(self, mobject, **kwargs):
        assert isinstance(mobject, PencilCreature)
        super().__init__(
            mobject, 
            rate_fct = exponential_decay,
            run_time = 0.5,
            direction = RIGHT,
            **kwargs,
        )


class BubbleIntroduction(AnimationGroup):
    
    def __init__(
        self, 
        creature, 
        content, 
        target_mode="ask",
        bubble_mode="speech",
        look_at_arg = None, 
        bubble_creation_class = Write,
        content_introduction_class= Write,
        **kwargs,
    ):

        bubble = creature.get_bubble(content, bubble_mode=bubble_mode)
        Group(bubble, bubble.content).shift_onto_screen()

        creature.generate_target()
        creature.target.change_mode(target_mode)
        if look_at_arg:
            creature.target.look_at(look_at_arg)

        change_mode = MoveToTarget(creature)
        bubble_creation = bubble_creation_class(bubble)
        content_introduction = content_introduction_class(bubble.content)
        AnimationGroup.__init__(
            self, change_mode, bubble_creation, content_introduction,
            **kwargs
        )


class Says(BubbleIntroduction):
    def __init__(self, creature, content, **kwargs):
        super().__init__(
            creature, 
            content, 
            target_mode="confident", 
            bubble_mode="speech",
            **kwargs
        )


class Asks(BubbleIntroduction):
    def __init__(self, creature, content, **kwargs):
        super().__init__(
            creature, 
            content, 
            target_mode="think", 
            bubble_mode="speech",
            **kwargs
        )


class Thinks(BubbleIntroduction):
    def __init__(self, creature, content, **kwargs):
        super().__init__(
            creature, 
            content, 
            target_mode="think", 
            bubble_mode="thought",
            **kwargs
        )


class RemoveBubble(BubbleIntroduction):

    def __init__(
        self, 
        creature, 
        look_at_arg = None,
        run_time= 0.5,
        **kwargs
    ):
        assert hasattr(creature, "bubble")

        if look_at_arg:
            creature.target.look_at(look_at_arg)

        AnimationGroup.__init__(
            self,
            Uncreate(creature.bubble),
            FadeOut(creature.bubble.content),
            run_time = run_time
        )

    # def clean_up_from_scene(self, scene=None):
    #     AnimationGroup.clean_up_from_scene(self, scene)
    #     self.creature.bubble = None
    #     if scene:
    #         scene.add(self.creature)

