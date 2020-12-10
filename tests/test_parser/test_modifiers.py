import inspect

from scc.actions import Action, AxisAction, ButtonAction, MouseAction
from scc.constants import HapticPos, SCButtons
from scc.modifiers import *
from scc.uinput import Axes, Keys

from . import _parse_compressed, _parses_as_itself


class TestModifiers(object):
    def test_tests(self):
        """
        Tests if this class has test for each known modifier defined.
        """
        for cls in Action.ALL.values():
            if "/modifiers.py" in inspect.getfile(cls):
                method_name = "test_%s" % (cls.COMMAND,)
                if not hasattr(self, method_name):
                    raise AssertionError(
                        "There is no test for %s modifier" % (cls.COMMAND)
                    )

    def test_name(self):
        """
        Tests if NameModifier is parsed
        """
        a = _parse_compressed("name('Not A Button', button(KEY_A))").compress()
        if not isinstance(a, ButtonAction):
            raise AssertionError
        if a.name != "Not A Button":
            raise AssertionError

    def test_click(self):
        """
        Tests if ClickModifier is parsed
        """
        a = _parse_compressed("click(button(KEY_A))")
        if not isinstance(a, ClickModifier):
            raise AssertionError

    def test_pressed(self):
        """
        Tests if ReleasedModifier is parsed
        """
        a = _parse_compressed("released(button(KEY_A))")
        if not isinstance(a, ReleasedModifier):
            raise AssertionError

    def test_released(self):
        """
        Tests if PressedModifier is parsed
        """
        a = _parse_compressed("pressed(axis(KEY_A))")
        if not isinstance(a, PressedModifier):
            raise AssertionError

    def test_touched(self):
        """
        Tests if TouchedModifier is parsed
        """
        a = _parse_compressed("touched(button(KEY_A))")
        if not isinstance(a, TouchedModifier):
            raise AssertionError

    def test_untouched(self):
        """
        Tests if UntouchedModifier is parsed
        """
        a = _parse_compressed("untouched(button(KEY_A))")
        if not isinstance(a, UntouchedModifier):
            raise AssertionError

    def test_circular(self):
        """
        Tests if CircularModifier is parsed
        """
        if not isinstance(_parse_compressed("circular(axis(ABS_X))"), CircularModifier):
            raise AssertionError
        if not isinstance(
            _parse_compressed("circular(axis(REL_WHEEL))"), CircularModifier
        ):
            raise AssertionError

    def test_circularabs(self):
        """
        Tests if CircularAbsModifier is parsed
        """
        if not isinstance(
            _parse_compressed("circularabs(axis(ABS_X))"), CircularAbsModifier
        ):
            raise AssertionError
        if not isinstance(
            _parse_compressed("circularabs(axis(REL_WHEEL))"), CircularAbsModifier
        ):
            raise AssertionError

    def test_ball(self):
        """
        Tests if BallModifier is parsed
        """
        a = _parse_compressed("ball(axis(ABS_X))")
        if not isinstance(a, BallModifier):
            raise AssertionError
        if not isinstance(a.action, AxisAction):
            raise AssertionError
        if a.action.id != Axes.ABS_X:
            raise AssertionError
        a = _parse_compressed("ball(mouse())")
        if not isinstance(a, BallModifier):
            raise AssertionError
        if not isinstance(a.action, MouseAction):
            raise AssertionError

    def test_smooth(self):
        """
        Tests if SmoothModifier is parsed
        """
        a = _parse_compressed("smooth(5, 0.3, axis(ABS_X))")
        if not isinstance(a, SmoothModifier):
            raise AssertionError
        if not isinstance(a.action, AxisAction):
            raise AssertionError
        if a.action.id != Axes.ABS_X:
            raise AssertionError
        if a.level != 5:
            raise AssertionError
        if a.multiplier != 0.3:
            raise AssertionError

    def test_deadzone(self):
        """
        Tests if DeadzoneModifier is parsed
        """
        # Lower only
        a = _parse_compressed("deadzone(100, axis(ABS_X))")
        if not isinstance(a, DeadzoneModifier):
            raise AssertionError
        if a.lower != 100 or a.upper != STICK_PAD_MAX:
            raise AssertionError
        if not isinstance(a.action, AxisAction):
            raise AssertionError
        if a.action.id != Axes.ABS_X:
            raise AssertionError
        # Lower and upper
        a = _parse_compressed("deadzone(100, 2000, axis(ABS_X))")
        if not isinstance(a, DeadzoneModifier):
            raise AssertionError
        if a.lower != 100 or a.upper != 2000:
            raise AssertionError
        if not isinstance(a.action, AxisAction):
            raise AssertionError
        if a.action.id != Axes.ABS_X:
            raise AssertionError

    def test_mode(self):
        """
        Tests if ModeModifier is parsed
        """
        # Without default
        a = _parse_compressed(
            """mode(
            A, axis(ABS_X),
            B, axis(ABS_Y)
        )"""
        )
        if not isinstance(a, ModeModifier):
            raise AssertionError
        if not isinstance(a.mods[SCButtons.A], AxisAction):
            raise AssertionError
        if a.mods[SCButtons.A].id != Axes.ABS_X:
            raise AssertionError

        # With default
        a = _parse_compressed(
            """mode(
            A, axis(ABS_X),
            B, axis(ABS_Y),
            button(KEY_A)
        )"""
        )
        if not isinstance(a, ModeModifier):
            raise AssertionError
        if not isinstance(a.mods[SCButtons.A], AxisAction):
            raise AssertionError
        if not isinstance(a.default, ButtonAction):
            raise AssertionError
        if a.default.button != Keys.KEY_A:
            raise AssertionError

    def test_doubleclick(self):
        """
        Tests if DoubleclickModifier is parsed
        """
        # With doubleclick action only
        a = _parse_compressed("doubleclick(axis(ABS_X))")
        if not (isinstance(a.action, AxisAction) and a.action.id == Axes.ABS_X):
            raise AssertionError
        if a.holdaction or a.normalaction:
            raise AssertionError
        # With doubleclick and normal action
        a = _parse_compressed("doubleclick(axis(ABS_X), axis(ABS_Y))")
        if not isinstance(a.action, AxisAction) or a.action.id != Axes.ABS_X:
            raise AssertionError
        if (
            not isinstance(a.normalaction, AxisAction)
            or a.normalaction.id != Axes.ABS_Y
        ):
            raise AssertionError
        if a.holdaction:
            raise AssertionError
        # With all parameters
        a = _parse_compressed("doubleclick(axis(ABS_X), axis(ABS_Y), 1.5)")
        if not (isinstance(a.action, AxisAction) and a.action.id == Axes.ABS_X):
            raise AssertionError
        if (
            not isinstance(a.normalaction, AxisAction)
            or a.normalaction.id != Axes.ABS_Y
        ):
            raise AssertionError
        if a.holdaction:
            raise AssertionError
        if a.timeout != 1.5:
            raise AssertionError

    def test_hold(self):
        """
        Tests if HoldModifier is parsed
        """
        # With hold action only
        a = _parse_compressed("hold(axis(ABS_X))")
        if not (isinstance(a.holdaction, AxisAction) and a.holdaction.id == Axes.ABS_X):
            raise AssertionError
        if a.action or a.normalaction:
            raise AssertionError
        # With hold and normal action
        a = _parse_compressed("hold(axis(ABS_X), axis(ABS_Y))")
        if not isinstance(a.holdaction, AxisAction) or a.holdaction.id != Axes.ABS_X:
            raise AssertionError
        if (
            not isinstance(a.normalaction, AxisAction)
            or a.normalaction.id != Axes.ABS_Y
        ):
            raise AssertionError
        if a.action:
            raise AssertionError
        # With all parameters
        a = _parse_compressed("hold(axis(ABS_X), axis(ABS_Y), 1.5)")
        if not (isinstance(a.holdaction, AxisAction) and a.holdaction.id == Axes.ABS_X):
            raise AssertionError
        if (
            not isinstance(a.normalaction, AxisAction)
            or a.normalaction.id != Axes.ABS_Y
        ):
            raise AssertionError
        if a.action:
            raise AssertionError
        if a.timeout != 1.5:
            raise AssertionError

    def test_hold_doubleclick_combinations(self):
        """
        Tests if combinations of DoubleclickModifier and HoldModifier
        are parsed as expected
        """
        a = _parse_compressed(
            "doubleclick(axis(ABS_X), hold(axis(ABS_Y), axis(ABS_Z)))"
        )
        if not (isinstance(a.action, AxisAction) and a.action.id == Axes.ABS_X):
            raise AssertionError
        if not (isinstance(a.holdaction, AxisAction) and a.holdaction.id == Axes.ABS_Y):
            raise AssertionError
        if (
            not isinstance(a.normalaction, AxisAction)
            or a.normalaction.id != Axes.ABS_Z
        ):
            raise AssertionError
        a = _parse_compressed(
            "hold(axis(ABS_X), doubleclick(axis(ABS_Y), axis(ABS_Z)))"
        )
        if not (isinstance(a.holdaction, AxisAction) and a.holdaction.id == Axes.ABS_X):
            raise AssertionError
        if not (isinstance(a.action, AxisAction) and a.action.id == Axes.ABS_Y):
            raise AssertionError
        if not (
            isinstance(a.normalaction, AxisAction) and a.normalaction.id == Axes.ABS_Z
        ):
            raise AssertionError
        a = _parse_compressed(
            "doubleclick(hold(axis(ABS_RX), axis(ABS_RY)), axis(ABS_Z))"
        )
        if not (isinstance(a.action, AxisAction) and a.action.id == Axes.ABS_RY):
            raise AssertionError
        if not isinstance(a.holdaction, AxisAction) or a.holdaction.id != Axes.ABS_RX:
            raise AssertionError
        if not (
            isinstance(a.normalaction, AxisAction) and a.normalaction.id == Axes.ABS_Z
        ):
            raise AssertionError
        a = _parse_compressed(
            "hold(doubleclick(axis(ABS_Z), axis(ABS_RZ)), axis(ABS_X))"
        )
        if not isinstance(a.action, AxisAction) or a.action.id != Axes.ABS_Z:
            raise AssertionError
        if not (
            isinstance(a.holdaction, AxisAction) and a.holdaction.id == Axes.ABS_RZ
        ):
            raise AssertionError
        if not (
            isinstance(a.normalaction, AxisAction) and a.normalaction.id == Axes.ABS_X
        ):
            raise AssertionError

    def test_sens(self):
        """
        Tests if SensitivityModifier can be converted to string and parsed
        back to same.
        """
        # Simple stuff
        if _parse_compressed("sens(2, axis(ABS_X))").strip().get_speed() != (2.0,):
            raise AssertionError
        if _parse_compressed("sens(2, 3, mouse())").strip().get_speed() != (2.0, 3.0):
            raise AssertionError
        if _parse_compressed(
            "sens(2, 3, 4, gyro(ABS_RZ, ABS_RX, ABS_Z))"
        ).strip().get_speed() != (2.0, 3.0, 4.0):
            raise AssertionError

        # Basic modifiers, sensitivity should always end applied to mouse() action
        a = _parse_compressed("sens(2, 3, click(mouse()))")
        if not isinstance(a.action, MouseAction) or a.action.get_speed() != (
            2.0,
            3.0,
        ):
            raise AssertionError
        a = _parse_compressed("sens(2, 3, deadzone(2.0, mouse()))")
        if not (
            isinstance(a.action, MouseAction) and a.action.get_speed() == (2.0, 3.0)
        ):
            raise AssertionError

        # Special case, sensitivity should be applied to ball(), not mouse()
        a = _parse_compressed("sens(2, 3, ball(mouse()))")
        if not isinstance(a.action, MouseAction) or a.action.get_speed() != (
            1.0,
            1.0,
        ):
            raise AssertionError
        if not isinstance(a, BallModifier) or a.get_speed() != (2.0, 3.0):
            raise AssertionError

    def test_feedback(self):
        """
        Tests if FeedbackModifier can be converted to string and parsed
        back to same.
        """
        # TODO: Here, with actual tests
        if not _parses_as_itself(FeedbackModifier(HapticPos.BOTH, MouseAction())):
            raise AssertionError
        if not _parses_as_itself(FeedbackModifier(HapticPos.BOTH, 10, MouseAction())):
            raise AssertionError
        if not _parses_as_itself(
            FeedbackModifier(HapticPos.BOTH, 10, 8, MouseAction())
        ):
            raise AssertionError
        if not _parses_as_itself(
            FeedbackModifier(HapticPos.BOTH, 10, 8, 512, MouseAction())
        ):
            raise AssertionError
        # Bellow was failing in past
        if not _parses_as_itself(FeedbackModifier(HapticPos.LEFT, MouseAction())):
            raise AssertionError
        if not _parses_as_itself(FeedbackModifier(HapticPos.RIGHT, MouseAction())):
            raise AssertionError

    def test_rotate(self):
        """
        Tests if RotateInputModifier can be converted to string and parsed
        back to same.
        """
        a = _parse_compressed("rotate(61, mouse())")
        if not isinstance(a, RotateInputModifier):
            raise AssertionError
