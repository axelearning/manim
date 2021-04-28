# from manimlib.animation.animation import Animation
# from manimlib.animation.composition import AnimationGroup
# from manimlib.animation.fading import FadeOut, FadeInFrom
# from manimlib.animation.creation import Write
# from manimlib.animation.transform import MoveToTarget, ApplyMethod
# from manimlib.constants import *
# from manimlib.mobject.mobject import Group
# from manimlib.mobject.svg.drawings import SpeechBubble
# from manimlib.utils.config_ops import digest_config
# from manimlib.utils.rate_functions import there_and_back, exponential_decay, squish_rate_func
# from manimlib.creature.pencil_creature import *

from manim.utils.rate_functions import squish_rate_func, there_and_back, exponential_decay
from manim.animation.transform import ApplyMethod
from manim.animation.fading import FadeInFrom, FadeOutAndShift
from manim.constants import *

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

# class BubbleIntroduction(AnimationGroup):
#     CONFIG = {
#         "target_mode": "ask",
#         "bubble_class": SpeechBubble,
#         "change_mode_kwargs": {},
#         "bubble_creation_class": Write,
#         "bubble_creation_kwargs": {},
#         "bubble_kwargs": {},
#         "content_introduction_class": Write,
#         "content_introduction_kwargs": {},
#         "look_at_arg": None,
#     }

#     def __init__(self, creature, *content, **kwargs):
#         digest_config(self, kwargs)
#         bubble = creature.get_bubble(
#             *content,
#             bubble_class=self.bubble_class,
#             **self.bubble_kwargs
#         )
#         Group(bubble, bubble.content).shift_onto_screen()

#         creature.generate_target()
#         creature.target.change_mode(self.target_mode)
#         if self.look_at_arg is not None:
#             creature.target.look_at(self.look_at_arg)

#         change_mode = MoveToTarget(creature, **self.change_mode_kwargs)
#         bubble_creation = self.bubble_creation_class(bubble, **self.bubble_creation_kwargs)
#         content_introduction = self.content_introduction_class(bubble.content, **self.content_introduction_kwargs)
#         AnimationGroup.__init__(
#             self, change_mode, bubble_creation, content_introduction,
#             **kwargs
#         )


# class Says(BubbleIntroduction):
#     CONFIG = {
#         "target_mode": "ask",
#         "bubble_class": SpeechBubble,
#     }


# class RemoveBubble(BubbleIntroduction):
#     CONFIG = {
#         "target_mode": "normal",
#         "look_at_arg": None,
#         "remover": True,
#         "run_time": 0.2
#     }

#     def __init__(self, creature, **kwargs):
#         assert hasattr(creature, "bubble")
#         digest_config(self, kwargs, locals())

#         # creature.generate_target()
#         # creature.target.change_mode(self.target_mode)
#         if self.look_at_arg is not None:
#             creature.target.look_at(self.look_at_arg)

#         AnimationGroup.__init__(
#             self,
#             # MoveToTarget(creature),
#             FadeOut(creature.bubble),
#             FadeOut(creature.bubble.content),
#             run_time = self.run_time
#         )

#     def clean_up_from_scene(self, scene=None):
#         AnimationGroup.clean_up_from_scene(self, scene)
#         self.creature.bubble = None
#         if scene is not None:
#             scene.add(self.creature)


# class FlashThroughClass(Animation):
#     CONFIG = {
#         "highlight_color": GREEN,
#     }

#     def __init__(self, mobject, mode="linear", **kwargs):
#         if not isinstance(mobject, PencilCreature):
#             raise Exception("FlashThroughClass mobject must be a PencilCreatureClass")
#         digest_config(self, kwargs)
#         self.indices = list(range(mobject.height * mobject.width))
#         if mode == "random":
#             np.random.shuffle(self.indices)
#         Animation.__init__(self, mobject, **kwargs)

#     def interpolate_mobject(self, alpha):
#         index = int(np.floor(alpha * self.mobject.height * self.mobject.width))
#         for pi in self.mobject:
#             pi.set_color(BLUE_E)
#         if index < self.mobject.height * self.mobject.width:
#             self.mobject[self.indices[index]].set_color(self.highlight_color)
