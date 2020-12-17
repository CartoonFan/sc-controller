import inspect

from . import _parses_as_itself
from scc.actions import ButtonAction
from scc.macros import *
from scc.uinput import Keys


class TestMacros(object):
    def test_tests(self):
        """
        Tests if this class has test for each known macro-related action defined.
        """
        for cls in list(Action.ALL.values()):
            if "/macros.py" in inspect.getfile(cls):
                method_name = "test_%s" % (cls.COMMAND, )
                if not hasattr(self, method_name):
                    raise AssertionError("There is no test for %s" %
                                         (cls.COMMAND))

    def test_macro(self):
        """
        Tests if Macro can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(
                Macro(
                    ButtonAction(Keys.BTN_LEFT),
                    ButtonAction(Keys.BTN_RIGHT),
                    ButtonAction(Keys.BTN_MIDDLE),
                )):
            raise AssertionError

    def test_type(self):
        """
        Tests if Type macro can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(Type("ilovecandy")):
            raise AssertionError

    def test_cycle(self):
        """
        Tests if Cycle can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(
                Cycle(
                    ButtonAction(Keys.BTN_LEFT),
                    ButtonAction(Keys.BTN_RIGHT),
                    ButtonAction(Keys.BTN_MIDDLE),
                )):
            raise AssertionError

    def test_repeat(self):
        """
        Tests if Repeat can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(Repeat(ButtonAction(Keys.BTN_LEFT))):
            raise AssertionError
        if not _parses_as_itself(
                Repeat(
                    Macro(
                        ButtonAction(Keys.BTN_LEFT),
                        ButtonAction(Keys.BTN_RIGHT),
                        ButtonAction(Keys.BTN_MIDDLE),
                    ))):
            raise AssertionError

    def test_sleep(self):
        """
        Tests if SleepAction can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(SleepAction(1.5)):
            raise AssertionError

    def test_press(self):
        """
        Tests if PressAction can be converted to string and
        parsed back to same action.
        """
        if not _parses_as_itself(PressAction(Keys.BTN_LEFT)):
            raise AssertionError

    def test_release(self):
        """
        Tests if ReleaseAction can be converted to string
        and parsed back to same action.
        """
        if not _parses_as_itself(ReleaseAction(Keys.BTN_LEFT)):
            raise AssertionError

    def test_tap(self):
        """
        Tests if TapAction can be converted to string
        and parsed back to same action.
        """
        if not _parses_as_itself(TapAction(Keys.BTN_LEFT)):
            raise AssertionError
