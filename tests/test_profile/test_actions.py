import inspect

from scc.actions import *
from scc.modifiers import BallModifier
from scc.uinput import Axes
from scc.uinput import Keys
from scc.uinput import Rels


class TestActions(object):

    # def test_tests(self):
    #   Tests if this class has test for every Action defined in actions.py.
    #   Removed: profile is not parsed this way anymore, so newly added actions
    #           don't have to support what's tested.

    def test_none(self):
        """
        Tests if empty json dict or dict without action is parsed NoAction.
        """
        if not isinstance(parser.from_json_data({}), NoAction):
            raise AssertionError
        if not isinstance(parser.from_json_data({"action": "None"}), NoAction):
            raise AssertionError
        if not isinstance(parser.from_json_data({"___": "Invalid"}), NoAction):
            raise AssertionError

    def test_axis(self):
        """
        Tests if AxisAction is parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "axis(ABS_X)"}),
                          AxisAction):
            raise AssertionError
        if parser.from_json_data({"action": "axis(ABS_X)"}).id != Axes.ABS_X:
            raise AssertionError

    def test_raxis(self):
        """
        Tests if RAxisAction is parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "raxis(ABS_X)"}),
                          RAxisAction):
            raise AssertionError
        if parser.from_json_data({"action": "raxis(ABS_X)"}).id != Axes.ABS_X:
            raise AssertionError

    def test_hats(self):
        """
        Tests if every Hat* actions can be parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "hatup(ABS_X)"}),
                          HatUpAction):
            raise AssertionError
        if not isinstance(parser.from_json_data({"action": "hatdown(ABS_X)"}),
                          HatDownAction):
            raise AssertionError
        if not isinstance(parser.from_json_data({"action": "hatleft(ABS_X)"}),
                          HatLeftAction):
            raise AssertionError
        if not isinstance(parser.from_json_data({"action": "hatright(ABS_X)"}),
                          HatRightAction):
            raise AssertionError

        if parser.from_json_data({"action": "hatup(ABS_X)"}).id != Axes.ABS_X:
            raise AssertionError
        if parser.from_json_data({
                "action": "hatdown(ABS_X)"
        }).id != Axes.ABS_X:
            raise AssertionError
        if parser.from_json_data({
                "action": "hatleft(ABS_X)"
        }).id != Axes.ABS_X:
            raise AssertionError
        if parser.from_json_data({
                "action": "hatright(ABS_X)"
        }).id != Axes.ABS_X:
            raise AssertionError

        if parser.from_json_data({"action": "hatup(ABS_X)"}).min != 0:
            raise AssertionError
        if parser.from_json_data({"action": "hatdown(ABS_X)"}).min != 0:
            raise AssertionError
        if parser.from_json_data({"action": "hatleft(ABS_X)"}).min != 0:
            raise AssertionError
        if parser.from_json_data({"action": "hatright(ABS_X)"}).min != 0:
            raise AssertionError

        if parser.from_json_data({
                "action": "hatup(ABS_X)"
        }).max != STICK_PAD_MIN + 1:
            raise AssertionError
        if parser.from_json_data({
                "action": "hatdown(ABS_X)"
        }).max != STICK_PAD_MAX - 1:
            raise AssertionError
        if parser.from_json_data({
                "action": "hatleft(ABS_X)"
        }).max != STICK_PAD_MIN + 1:
            raise AssertionError
        if (parser.from_json_data({
                "action": "hatright(ABS_X)"
        }).max != STICK_PAD_MAX - 1):
            raise AssertionError

    def test_mouse(self):
        """
        Tests if MouseAction is parsed correctly from json.
        """
        if parser.from_json_data({
                "action": "mouse()"
        })._mouse_axis is not None:
            raise AssertionError
        if parser.from_json_data({
                "action": "trackpad()"
        })._mouse_axis is not None:
            raise AssertionError
        if (parser.from_json_data({
                "action": "mouse(REL_WHEEL)"
        })._mouse_axis != Rels.REL_WHEEL):
            raise AssertionError

    def test_mouseabs(self):
        """
        Tests if MouseAction is parsed correctly from json.
        """
        if (parser.from_json_data({
                "action": "mouseabs(REL_X)"
        })._mouse_axis != Rels.REL_X):
            raise AssertionError
        if parser.from_json_data({
                "action": "mouseabs()"
        })._mouse_axis is not None:
            raise AssertionError

    def test_area(self):
        """
        Tests if AreaAction are parsed correctly from json.
        """
        if not isinstance(
                parser.from_json_data({"action": "area(10, 10, 50, 50)"}),
                AreaAction):
            raise AssertionError
        if parser.from_json_data({
                "action": "area(10, 10, 50, 50)"
        }).coords != (
                10,
                10,
                50,
                50,
        ):
            raise AssertionError

    def test_relarea(self):
        """
        Tests if  RelAreaAction are parsed correctly from json.
        """
        if not isinstance(
                parser.from_json_data({"action": "relarea(10, 10, 50, 50)"}),
                RelAreaAction):
            raise AssertionError
        if parser.from_json_data({
                "action": "relarea(10, 10, 50, 50)"
        }).coords != (
                10,
                10,
                50,
                50,
        ):
            raise AssertionError

    def test_winarea(self):
        """
        Tests if WinAreaAction are parsed correctly from json.
        """
        if not isinstance(
                parser.from_json_data({"action": "winarea(10, 10, 50, 50)"}),
                WinAreaAction):
            raise AssertionError
        if parser.from_json_data({
                "action": "winarea(10, 10, 50, 50)"
        }).coords != (
                10,
                10,
                50,
                50,
        ):
            raise AssertionError

    def test_relwinarea(self):
        """
        Tests if RelWinAreaAction are parsed correctly from json.
        """
        if not isinstance(
                parser.from_json_data({"action": "relwinarea(10, 10, 50, 50)"
                                       }),
                RelWinAreaAction,
        ):
            raise AssertionError
        if parser.from_json_data({
                "action": "relwinarea(10, 10, 50, 50)"
        }).coords != (
                10,
                10,
                50,
                50,
        ):
            raise AssertionError

    def test_gyro(self):
        """
        Tests if GyroAction is parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "gyro(ABS_X)"}),
                          GyroAction):
            raise AssertionError

        if parser.from_json_data({
                "action": "gyro(ABS_X)"
        }).axes[0] != Axes.ABS_X:
            raise AssertionError
        if parser.from_json_data({
                "action": "gyro(ABS_X)"
        }).axes[1] is not None:
            raise AssertionError
        if (parser.from_json_data({
                "action": "gyro(ABS_X, ABS_Y)"
        }).axes[1] != Axes.ABS_Y):
            raise AssertionError
        if parser.from_json_data({
                "action": "gyro(ABS_X, ABS_Y)"
        }).axes[2] is not None:
            raise AssertionError
        if (parser.from_json_data({
                "action": "gyro(ABS_X, ABS_Y, ABS_Z)"
        }).axes[2] != Axes.ABS_Z):
            raise AssertionError

    def test_gyroabs(self):
        """
        Tests if GyroAbsAction is parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "gyroabs(ABS_X)"}),
                          GyroAbsAction):
            raise AssertionError

        if parser.from_json_data({
                "action": "gyroabs(ABS_X)"
        }).axes[0] != Axes.ABS_X:
            raise AssertionError
        if parser.from_json_data({
                "action": "gyroabs(ABS_X)"
        }).axes[1] is not None:
            raise AssertionError
        if (parser.from_json_data({
                "action": "gyroabs(ABS_X, ABS_Y)"
        }).axes[1] != Axes.ABS_Y):
            raise AssertionError
        if (parser.from_json_data({
                "action": "gyroabs(ABS_X, ABS_Y)"
        }).axes[2] is not None):
            raise AssertionError
        if (parser.from_json_data({
                "action": "gyroabs(ABS_X, ABS_Y, ABS_Z)"
        }).axes[2] != Axes.ABS_Z):
            raise AssertionError

    def test_resetgyro(self):
        """
        Tests if ResetGyroAction is parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "resetgyro()"}),
                          ResetGyroAction):
            raise AssertionError

    def test_tilt(self):
        """
        Tests if TiltAction can be converted to string and
        parsed back to same action.
        """
        # With only one button
        if (parser.from_json_data({
                "action": "tilt( button(KEY_D) )"
        }).actions[0].button != Keys.KEY_D):
            raise AssertionError

        # With all buttons
        if (parser.from_json_data({
                "action":
                "tilt( button(KEY_D), button(KEY_U), button(KEY_L), button(KEY_R))"
        }).actions[3].button != Keys.KEY_R):
            raise AssertionError

    def test_trackball(self):
        """
        Tests if TrackballAction is parsed correctly from json.
        """
        # assert isinstance(parser.from_json_data({ 'action' : 'trackball' }), TrackballAction)
        a = parser.from_json_data({"action": "trackball"})
        if not isinstance(a, BallModifier):
            raise AssertionError
        if not isinstance(a.action, MouseAction):
            raise AssertionError

    def test_button(self):
        """
        Tests if ButtonAction is parsed correctly from json.
        """
        if not isinstance(parser.from_json_data({"action": "button(KEY_X)"}),
                          ButtonAction):
            raise AssertionError

        if parser.from_json_data({
                "action": "button(KEY_X)"
        }).button != Keys.KEY_X:
            raise AssertionError
        if parser.from_json_data({
                "action": "button(KEY_X)"
        }).button2 is not None:
            raise AssertionError
        if (parser.from_json_data({
                "action": "button(KEY_X, KEY_Z)"
        }).button != Keys.KEY_X):
            raise AssertionError
        if (parser.from_json_data({
                "action": "button(KEY_X, KEY_Z)"
        }).button2 != Keys.KEY_Z):
            raise AssertionError

    def test_multiaction(self):
        """
        Tests if MultiAction is parsed correctly from json.
        """
        a = parser.from_json_data(
            {"action": "button(KEY_X) and button(KEY_Y)"})
        if not isinstance(a, MultiAction):
            raise AssertionError
        if not isinstance(a.actions[0], ButtonAction):
            raise AssertionError
        if a.actions[0].button != Keys.KEY_X:
            raise AssertionError
        if not isinstance(a.actions[1], ButtonAction):
            raise AssertionError
        if a.actions[1].button != Keys.KEY_Y:
            raise AssertionError

    def test_dpad(self):
        """
        Tests if DPadAction is parsed correctly from json.
        """
        a = parser.from_json_data({
            "dpad": [
                {
                    "action": "button(KEY_A)"
                },
                {
                    "action": "button(KEY_B)"
                },
                {
                    "action": "button(KEY_C)"
                },
                {
                    "action": "button(KEY_D)"
                },
            ]
        })

        if not isinstance(a, DPadAction):
            raise AssertionError
        for sub in a.actions:
            if not isinstance(sub, ButtonAction):
                raise AssertionError

    def test_ring(self):
        """
        Tests if DPadAction is parsed correctly from json.
        """
        a = parser.from_json_data({
            "ring": {
                "radius": 0.3,
                "outer": {
                    "dpad": [
                        {
                            "action": "button(KEY_A)"
                        },
                        {
                            "action": "button(KEY_B)"
                        },
                        {
                            "action": "button(KEY_C)"
                        },
                        {
                            "action": "button(KEY_D)"
                        },
                    ]
                },
                "inner": {
                    "X": {
                        "action": "axis(ABS_X)"
                    },
                    "Y": {
                        "action": "axis(ABS_Y)"
                    },
                },
            }
        })

        if not isinstance(a.outer, DPadAction):
            raise AssertionError
        for sub in a.outer.actions:
            if not isinstance(sub, ButtonAction):
                raise AssertionError
        if not isinstance(a.inner, XYAction):
            raise AssertionError
        for sub in a.inner.actions:
            if not isinstance(sub, AxisAction):
                raise AssertionError

    def test_dpad8(self):
        """
        Tests if DPad8Action is parsed correctly from json.
        """
        a = parser.from_json_data({
            "dpad": [
                {
                    "action": "button(KEY_A)"
                },
                {
                    "action": "button(KEY_B)"
                },
                {
                    "action": "button(KEY_C)"
                },
                {
                    "action": "button(KEY_D)"
                },
                {
                    "action": "button(KEY_E)"
                },
                {
                    "action": "button(KEY_F)"
                },
                {
                    "action": "button(KEY_G)"
                },
                {
                    "action": "button(KEY_H)"
                },
            ]
        })

        print(a)
        print(a.actions)
        if not isinstance(a, DPadAction):
            raise AssertionError
        for sub in a.actions:
            if not isinstance(sub, ButtonAction):
                raise AssertionError

    def test_XY(self):
        """
        Tests if XYAction is parsed correctly from json.
        """
        a = parser.from_json_data({
            "X": {
                "action": "axis(ABS_X)"
            },
            "Y": {
                "action": "axis(ABS_Y)"
            },
        })

        if not isinstance(a, XYAction):
            raise AssertionError
        if not isinstance(a.x, AxisAction):
            raise AssertionError
        if not isinstance(a.y, AxisAction):
            raise AssertionError

    def test_trigger(self):
        """
        Tests if TriggerAction is parsed correctly from json.
        """
        a = parser.from_json_data({
            "action": "button(KEY_X)",
            "levels": [10, 80]
        })

        if not isinstance(a, TriggerAction):
            raise AssertionError
        if not isinstance(a.action, ButtonAction):
            raise AssertionError
        if a.press_level != 10:
            raise AssertionError
        if a.release_level != 80:
            raise AssertionError
