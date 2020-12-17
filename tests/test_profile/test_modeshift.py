from scc.constants import SCButtons
from scc.modifiers import *

from . import parser


class TestModeshift(object):
    """
    Tests various combinations of modeshift and modifiers.
    Most are based on stuff that was failing in past.
    """

    def test_146_1(self):
        """
        https://github.com/kozec/sc-controller/issues/146
        """
        STR = "mode(LB, dpad(button(Keys.KEY_UP)), rotate(3.8, sens(2.0, 2.0, ball(0.552, mouse()))))"
        a = parser.from_json_data(
            {
                "action": "mouse()",
                "ball": [0.552],
                "rotate": 3.8,
                "sensitivity": [2.0, 2.0, 1.0],
                "modes": {"LB": {"dpad": [{"action": "button(Keys.KEY_UP)"}]}},
            }
        )

        if a.to_string() != STR:
            raise AssertionError
        if not isinstance(a, ModeModifier):
            raise AssertionError
        if not isinstance(a.default, RotateInputModifier):
            raise AssertionError
        sens = a.default.action
        if not isinstance(sens, SensitivityModifier):
            raise AssertionError
        if tuple(sens.speeds) != (2.0, 2.0, 1.0):
            raise AssertionError
        ball = sens.action
        if not isinstance(ball, BallModifier):
            raise AssertionError
        if ball.friction != 0.552:
            raise AssertionError

    def test_146_2(self):
        """
        https://github.com/kozec/sc-controller/issues/146
        """
        STR = "mode(LGRIP, ball(XY(mouse(Rels.REL_HWHEEL), mouse(Rels.REL_WHEEL))), rotate(3.8, sens(2.0, 2.0, mouse())))"
        a = parser.from_json_data(
            {
                "action": "mouse()",
                "rotate": 3.8,
                "sensitivity": [2.0, 2.0, 1.0],
                "modes": {
                    "LGRIP": {
                        "X": {"action": "mouse(Rels.REL_HWHEEL)"},
                        "Y": {"action": "mouse(Rels.REL_WHEEL)"},
                        "ball": [],
                    }
                },
            }
        )

        if a.to_string() != STR:
            raise AssertionError
        if not isinstance(a, ModeModifier):
            raise AssertionError
        if not isinstance(a.default, RotateInputModifier):
            raise AssertionError
        sens = a.default.action
        if not isinstance(sens, SensitivityModifier):
            raise AssertionError
        if tuple(sens.speeds) != (2.0, 2.0, 1.0):
            raise AssertionError
        lgrip = a.mods[SCButtons.LGRIP]
        if not isinstance(lgrip, BallModifier):
            raise AssertionError
        if not isinstance(lgrip.action, XYAction):
            raise AssertionError
