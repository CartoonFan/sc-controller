import inspect

from . import parser
from scc.actions import AxisAction
from scc.actions import GyroAction
from scc.constants import HapticPos
from scc.constants import SCButtons
from scc.modifiers import *
from scc.uinput import Axes


def _is_axis_with_value(a, value=Axes.ABS_X):
    """
    Common part of all tests; Check if parsed action
    is AxisAction with given value as parameter.
    """
    if not isinstance(a, AxisAction):
        raise AssertionError
    if a.id != value:
        raise AssertionError
    return True


class TestModifiers(object):
    def test_tests(self):
        """
        Tests if this class has test for each known modifier defined.
        """
        for cls in list(Action.ALL.values()):
            if "/modifiers.py" in inspect.getfile(cls):
                method_name = "test_%s" % (cls.COMMAND,)
                if not hasattr(self, method_name):
                    raise AssertionError(
                        "There is no test for %s modifier" % (cls.COMMAND)
                    )

    def test_name(self):
        """
        Tests if NameModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "axis(ABS_X)", "name": "hithere"})

        # NameModifier is lost in parsing
        if isinstance(a, NameModifier):
            raise AssertionError
        if a.name != "hithere":
            raise AssertionError
        if not _is_axis_with_value(a):
            raise AssertionError

    def test_click(self):
        """
        Tests if ClickModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "axis(ABS_X)", "click": True})

        if not isinstance(a, ClickModifier):
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_pressed(self):
        """
        Tests if PressedModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "pressed(axis(ABS_X))"})
        if not isinstance(a, PressedModifier):
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_released(self):
        """
        Tests if ReleasedModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "released(axis(ABS_X))"})
        if not isinstance(a, ReleasedModifier):
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_touched(self):
        """
        Tests if TouchedModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "touched(button(KEY_A))"})
        if not isinstance(a, TouchedModifier):
            raise AssertionError

    def test_untouched(self):
        """
        Tests if UntouchedModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "untouched(button(KEY_A))"})
        if not isinstance(a, UntouchedModifier):
            raise AssertionError

    def test_circular(self):
        """
        Tests if CircularModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "axis(ABS_X)", "circular": True})
        if not isinstance(a, CircularModifier):
            raise AssertionError

    def test_circularabs(self):
        """
        Tests if CircularModifier is parsed correctly from json.
        """
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "circularabs": True})
        if not isinstance(a, CircularAbsModifier):
            raise AssertionError

    def test_ball(self):
        """
        Tests if BallModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "axis(ABS_X)", "ball": True})

        if not isinstance(a, BallModifier):
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_smooth(self):
        """
        Tests if SmoothModifier is parsed correctly from json.
        """
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "smooth": [5, 0.3]})

        if not isinstance(a, SmoothModifier):
            raise AssertionError
        if a.level != 5:
            raise AssertionError
        if a.multiplier != 0.3:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_deadzone(self):
        """
        Tests if DeadzoneModifier is parsed correctly from json.
        """
        # One parameter
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "deadzone": {"upper": 300}})

        if not isinstance(a, DeadzoneModifier):
            raise AssertionError
        if a.upper != 300:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

        # Two parameters
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "deadzone": {"upper": 300, "lower": 50}}
        )

        if not isinstance(a, DeadzoneModifier):
            raise AssertionError
        if a.lower != 50:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_sens(self):
        """
        Tests if SensitivityModifier is parsed correctly from json.
        """
        # Simple
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "sensitivity": [2.0, 3.0, 4.0]}
        )
        if not isinstance(a, SensitivityModifier):
            raise AssertionError
        if a.speeds != [2.0, 3.0, 4.0]:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

        # Hold and doubleclick
        a = parser.from_json_data(
            {
                "hold": {"action": "mouse(ROLL)", "sensitivity": [3.0, 4.0]},
                "doubleclick": {
                    "action": "gyro(ABS_RZ, ABS_RX, ABS_Z)",
                    "sensitivity": [7.0, 8.0, 9.0],
                },
                "action": "axis(ABS_Z)",
                "sensitivity": [
                    10.0,
                ],
            }
        ).compress()
        if not (
            isinstance(a.holdaction, MouseAction)
            and a.holdaction.get_speed() == (3.0, 4.0)
        ):
            raise AssertionError
        if not (
            isinstance(
                a.action,
                GyroAction) and a.action.get_speed() == (
                7.0,
                8.0,
                9.0)):
            raise AssertionError
        if not (
            isinstance(a.normalaction, AxisAction)
            and a.normalaction.get_speed() == (10.0,)
        ):
            raise AssertionError

        # Modeshift
        a = parser.from_json_data(
            {
                "modes": {
                    "A": {"action": "mouse(ROLL)", "sensitivity": [3.0, 4.0]},
                    "B": {
                        "action": "axis(ABS_X)",
                        "sensitivity": [
                            7.0,
                        ],
                    },
                    "X": {
                        "action": "gyro(ABS_RZ, ABS_RX, ABS_Z)",
                        "sensitivity": [8.0, 9.0, 10.0],
                    },
                },
                "action": "axis(ABS_Z)",
                "sensitivity": [
                    12.0,
                ],
            }
        ).compress()
        if not (
            isinstance(a.mods[SCButtons.A], MouseAction)
            and a.mods[SCButtons.A].get_speed() == (3.0, 4.0)
        ):
            raise AssertionError
        if not (
            isinstance(a.mods[SCButtons.B], AxisAction)
            and a.mods[SCButtons.B].get_speed() == (7.0,)
        ):
            raise AssertionError
        if not (
            isinstance(a.mods[SCButtons.X], GyroAction)
            and a.mods[SCButtons.X].get_speed() == (8.0, 9.0, 10.0)
        ):
            raise AssertionError
        if not (
                isinstance(
                    a.default,
                    AxisAction) and a.default.get_speed() == (
                    12.0,
                )):
            raise AssertionError

    def test_feedback(self):
        """
        Tests if FeedbackModifier is parsed correctly from json.
        """
        # One parameter
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "feedback": ["BOTH"]})

        if not isinstance(a, FeedbackModifier):
            raise AssertionError
        if a.haptic.get_position() != HapticPos.BOTH:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

        # All parameters
        a = parser.from_json_data(
            {"action": "axis(ABS_X)", "feedback": ["RIGHT", 1024, 8, 2048]}
        )

        if not isinstance(a, FeedbackModifier):
            raise AssertionError
        if a.haptic.get_position() != HapticPos.RIGHT:
            raise AssertionError
        if a.haptic.get_amplitude() != 1024:
            raise AssertionError
        if a.haptic.get_frequency() != 8:
            raise AssertionError
        if a.haptic.get_period() != 2048:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_rotate(self):
        """
        Tests if RotateInputModifier is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "axis(ABS_X)", "rotate": 33.14})

        if not isinstance(a, RotateInputModifier):
            raise AssertionError
        if a.angle != 33.14:
            raise AssertionError
        if not _is_axis_with_value(a.action):
            raise AssertionError

    def test_mode(self):
        """
        Tests if ModeModifier is parsed correctly from json.
        """
        # Without default
        a = parser.from_json_data(
            {
                "modes": {
                    "A": {"action": "axis(ABS_X)"},
                    "B": {"action": "axis(ABS_Y)"},
                    "LT": {"action": "axis(ABS_Z)"},
                }
            }
        )

        if not isinstance(a, ModeModifier):
            raise AssertionError
        if not _is_axis_with_value(a.mods[SCButtons.A], Axes.ABS_X):
            raise AssertionError
        if not _is_axis_with_value(a.mods[SCButtons.B], Axes.ABS_Y):
            raise AssertionError
        if not _is_axis_with_value(a.mods[SCButtons.LT], Axes.ABS_Z):
            raise AssertionError

        # With default
        a = parser.from_json_data(
            {
                "action": "axis(ABS_RX)",
                "modes": {
                    "X": {"action": "axis(ABS_X)"},
                    "RT": {"action": "axis(ABS_Z)"},
                },
            }
        )

        if not isinstance(a, ModeModifier):
            raise AssertionError
        if not _is_axis_with_value(a.default, Axes.ABS_RX):
            raise AssertionError
        if not _is_axis_with_value(a.mods[SCButtons.X], Axes.ABS_X):
            raise AssertionError
        if not _is_axis_with_value(a.mods[SCButtons.RT], Axes.ABS_Z):
            raise AssertionError

    def test_doubleclick(self):
        """
        Tests if DoubleclickModifier is parsed correctly from json.
        """
        a = parser.from_json_data(
            {"action": "axis(ABS_RX)", "doubleclick": {"action": "axis(ABS_X)"}}
        )

        if not isinstance(a, DoubleclickModifier):
            raise AssertionError
        if not _is_axis_with_value(a.normalaction, Axes.ABS_RX):
            raise AssertionError
        if not _is_axis_with_value(a.action, Axes.ABS_X):
            raise AssertionError
        if a.holdaction:
            raise AssertionError

    def test_hold(self):
        """
        Tests if HoldModifier is parsed correctly from json.
        """
        a = parser.from_json_data(
            {"action": "axis(ABS_RX)", "hold": {"action": "axis(ABS_X)"}}
        )

        if not isinstance(a, HoldModifier):
            raise AssertionError
        if not _is_axis_with_value(a.normalaction, Axes.ABS_RX):
            raise AssertionError
        if not _is_axis_with_value(a.holdaction, Axes.ABS_X):
            raise AssertionError
        if a.action:
            raise AssertionError
