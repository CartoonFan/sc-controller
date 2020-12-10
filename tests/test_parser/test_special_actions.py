import inspect

from scc.constants import STICK, SCButtons
from scc.special_actions import *

from . import _parses_as_itself

MENU_CLASSES = (
    MenuAction,
    HorizontalMenuAction,
    GridMenuAction,
    RadialMenuAction,
    QuickMenuAction,
)


class TestSpecialActions(object):
    def test_tests(self):
        """
        Tests if this class has test for each known SpecialAction defined.
        """
        for cls in list(Action.ALL.values()):
            if "/special_actions.py" in inspect.getfile(cls):
                if cls in MENU_CLASSES:
                    # Skip over some hard-coded cases, these have
                    # tests merged together under weird names
                    continue
                method_name = "test_%s" % (cls.COMMAND,)
                if not hasattr(self, method_name):
                    raise AssertionError("There is no test for %s" % (cls.COMMAND))

    def test_profile(self):
        """
        Tests if ChangeProfileAction can be converted to string and parsed
        back to same action.
        """
        if not _parses_as_itself(ChangeProfileAction("profile")):
            raise AssertionError

    def test_shell(self):
        """
        Tests if ShellAction can be converted to string and parsed
        back to same action.
        """
        if not _parses_as_itself(ShellCommandAction("ls -la")):
            raise AssertionError

    def test_turnoff(self):
        """
        Tests if TurnOffAction can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(TurnOffAction()):
            raise AssertionError

    def test_restart(self):
        """
        Tests if RestartDaemonAction can be converted to string and parsed
        back to same action.
        """
        if not _parses_as_itself(RestartDaemonAction()):
            raise AssertionError

    def test_led(self):
        """
        Tests if LockedAction can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(LedAction(66)):
            raise AssertionError

    def test_osd(self):
        """
        Tests if OSDAction can be converted to string and parsed back to
        same action.
        """
        # With text
        if not _parses_as_itself(OSDAction("Hello")):
            raise AssertionError
        # With subaction
        if not _parses_as_itself(OSDAction(TurnOffAction())):
            raise AssertionError

    def test_clearosd(self):
        """
        Tests if ClearOSDAction can be converted to string and parsed back to
        same action.
        """
        # With text
        if not _parses_as_itself(ClearOSDAction()):
            raise AssertionError

    def test_menus(self):
        """
        Tests if all Menu*Actions can be converted to string and parsed
        back to same action.
        """
        for cls in MENU_CLASSES:
            # Simple
            if not _parses_as_itself(cls("menu1")):
                raise AssertionError
            # With arguments
            if not _parses_as_itself(cls("menu1", STICK)):
                raise AssertionError
            if not _parses_as_itself(cls("menu1", STICK, SCButtons.X)):
                raise AssertionError
            if not _parses_as_itself(cls("menu1", STICK, SCButtons.X, SCButtons.Y)):
                raise AssertionError
            if not _parses_as_itself(
                cls("menu1", STICK, SCButtons.X, SCButtons.Y, True)
            ):
                raise AssertionError

    def test_dialog(self):
        """
        Tests if all Menu*Actions can be converted to string and parsed
        back to same action.
        """
        if not _parses_as_itself(
            DialogAction("Some Text", NameModifier("Option", OSDAction("display this")))
        ):
            raise AssertionError
        if not _parses_as_itself(
            DialogAction(
                SCButtons.X,
                "Some Text",
                NameModifier("Option", OSDAction("display this")),
            )
        ):
            raise AssertionError
        if not _parses_as_itself(
            DialogAction(
                SCButtons.X,
                SCButtons.Y,
                "Some Text",
                NameModifier("Option", OSDAction("display this")),
            )
        ):
            raise AssertionError

    def test_position(self):
        """
        Tests if PositionModifier can be converted to string and parsed
        back to same action.
        """
        if not _parses_as_itself(PositionModifier(14, -34, MenuAction("menu1"))):
            raise AssertionError

    def test_keyboard(self):
        """
        Tests if KeyboardAction can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(KeyboardAction()):
            raise AssertionError

    def test_gestures(self):
        """
        Tests if GesturesAction can be converted to string and parsed back to
        same action.
        """
        if not _parses_as_itself(
            GesturesAction("UUDD", KeyboardAction(), "LRLR", TurnOffAction())
        ):
            raise AssertionError

    def test_cemuhook(self):
        """
        Nothing to test here
        """
        pass
