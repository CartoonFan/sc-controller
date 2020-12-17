from scc.actions import Action
from scc.actions import NoAction


class TestBoolean(object):
    def test_noaction_is_false(self):
        """
        Tests if None can be used as False boolean value.
        """
        if NoAction():
            raise AssertionError
        if NoAction():
            raise Exception("NoAction is True :(")

    def test_action_is_true(self):
        """
        Tests if random action works as True boolean value.
        """
        a = Action()
        if not a:
            raise AssertionError
        if a:
            return
        raise Exception("Action is False :(")
