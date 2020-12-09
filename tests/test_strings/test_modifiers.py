import inspect

from . import _parses_as
from scc.actions import AxisAction
from scc.modifiers import *
from scc.uinput import Axes


class TestModifiers(object):

    # TODO: Much more tests
    # TODO: test_tests

    def test_ball(self):
        """
        Tests if BallModifier can be converted from string
        """
        # All options
        if not _parses_as(
                "ball(15, 40, 15, 0.1, 3265, 4, axis(ABS_X))",
                BallModifier(15, 40, 15, 0.1, 3265, 4, AxisAction(Axes.ABS_X)),
        ):
            raise AssertionError
