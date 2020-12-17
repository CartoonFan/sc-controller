from . import parser
from scc.actions import ButtonAction
from scc.constants import HapticPos
from scc.constants import SCButtons
from scc.special_actions import *

MENU_CLASSES = (
    MenuAction,
    HorizontalMenuAction,
    GridMenuAction,
    RadialMenuAction,
    QuickMenuAction,
)


class TestSpecialActions(object):

    # def test_tests(self):
    # 	Tests if this class has test for each known SpecialAction defined.
    # 	Removed: profile is not parsed this way anymore, so newly added actions
    # 			don't have to support what's tested.

    def test_profile(self):
        """
        Tests if ChangeProfileAction is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "profile('xyz')"})
        if not isinstance(a, ChangeProfileAction):
            raise AssertionError
        if a.profile != "xyz":
            raise AssertionError

    def test_shell(self):
        """
        Tests if ShellCommandAction is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "shell('ls -la')"})
        if not isinstance(a, ShellCommandAction):
            raise AssertionError
        if a.command != "ls -la":
            raise AssertionError

    def test_turnoff(self):
        """
        Tests if TurnOffAction is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "turnoff"})
        if not isinstance(a, TurnOffAction):
            raise AssertionError

    def test_restart(self):
        """
        Tests if RestartDaemonAction is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "restart"})
        if not isinstance(a, RestartDaemonAction):
            raise AssertionError

    def test_led(self):
        """
        Tests if LockedAction is parsed correctly from json.
        """
        a = parser.from_json_data({"action": "led(66)"})
        if not isinstance(a, LedAction):
            raise AssertionError
        if a.brightness != 66:
            raise AssertionError

    def test_osd(self):
        """
        Tests if OSDAction is parsed correctly from json.
        """
        # With text
        a = parser.from_json_data({"action": "osd('something')"})
        if not isinstance(a, OSDAction):
            raise AssertionError
        if a.text != "something":
            raise AssertionError
        # As modifier
        a = parser.from_json_data({"action": "button(KEY_X)", "osd": True})
        if not isinstance(a, OSDAction):
            raise AssertionError
        if not isinstance(a.action, ButtonAction):
            raise AssertionError

    def test_dialog(self):
        """
        Tests if all Menu*Actions are parsed correctly from json.
        """
        # Simple
        a = parser.from_json_data({"action": "dialog('title', osd('something'))"})
        if not isinstance(a, DialogAction):
            raise AssertionError
        if a.text != "title":
            raise AssertionError
        if len(a.options) != 1:
            raise AssertionError
        if not isinstance(a.options[0], OSDAction):
            raise AssertionError
        if a.options[0].text != "something":
            raise AssertionError

        # Complete
        a = parser.from_json_data(
            {
                "action": "dialog(X, Y, 'title', "
                "name('button', osd('something')), name('item', osd('something else')))"
            }
        )
        if a.confirm_with != SCButtons.X:
            raise AssertionError
        if a.cancel_with != SCButtons.Y:
            raise AssertionError
        if not isinstance(a, DialogAction):
            raise AssertionError
        if a.text != "title":
            raise AssertionError
        if len(a.options) != 2:
            raise AssertionError
        if a.options[0].describe(Action.AC_MENU) != "button":
            raise AssertionError
        if a.options[0].strip().text != "something":
            raise AssertionError

    def test_menus(self):
        """
        Tests if all Menu*Actions are parsed correctly from json.
        """
        for cls in MENU_CLASSES:
            a_str = "%s('some.menu', LEFT, X, Y, True)" % (cls.COMMAND,)
            a = parser.from_json_data({"action": a_str})
            if not isinstance(a, cls):
                raise AssertionError
            if a.control_with != HapticPos.LEFT:
                raise AssertionError
            if a.confirm_with != SCButtons.X:
                raise AssertionError
            if a.cancel_with != SCButtons.Y:
                raise AssertionError
            if a.show_with_release is True:
                raise AssertionError

    def test_position(self):
        """
        Tests if PositionModifier is parsed correctly from json.
        """
        a = parser.from_json_data(
            {"action": "menu('some.menu', LEFT, X, Y, True)", "position": [-10, 10]}
        ).compress()

        if not isinstance(a, MenuAction):
            raise AssertionError
        if a.x != -10:
            raise AssertionError
        if a.y != 10:
            raise AssertionError

    def test_keyboard(self):
        """
        Tests if KeyboardAction is parsed correctly from json.
        """
        # With text
        a = parser.from_json_data({"action": "keyboard"})
        if not isinstance(a, KeyboardAction):
            raise AssertionError

    def test_gestures(self):
        """
        Tests if GesturesAction is parsed correctly from json.
        """
        # Simple
        a = parser.from_json_data(
            {"gestures": {"UD": {"action": "turnoff"}, "LR": {"action": "keyboard"}}}
        )
        if not isinstance(a, GesturesAction):
            raise AssertionError
        if not isinstance(a.gestures["UD"], TurnOffAction):
            raise AssertionError
        if not isinstance(a.gestures["LR"], KeyboardAction):
            raise AssertionError
        # With OSD
        a = parser.from_json_data(
            {
                "gestures": {
                    "UD": {"action": "turnoff"},
                },
                "osd": True,
            }
        )
        if not isinstance(a, OSDAction):
            raise AssertionError
        if not isinstance(a.action, GesturesAction):
            raise AssertionError
        if not isinstance(a.action.gestures["UD"], TurnOffAction):
            raise AssertionError

    def test_cemuhook(self):
        """
        Nothing to test here
        """
        pass
