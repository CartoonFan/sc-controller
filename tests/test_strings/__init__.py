import sys

from scc.actions import Action
from scc.parser import ActionParser

parser = ActionParser()


def _parses_as(a_str, action):
    """
    Tests if action parsed from string equals specified action.

    Done by parsing string to Action and comparing it using _same_action()
    """
    parsed = parser.restart(a_str).parse()
    if not _same_action(parsed, action):
        raise AssertionError
    return True


def _same_action(a1, a2):
    """
    Tests if two actions are the same.
    Done by comparing .parameters list and .to_string() output.
    """
    if len(a1.parameters) != len(a2.parameters):
        raise AssertionError
    for i in range(0, len(a1.parameters)):
        if isinstance(a1.parameters[i], Action):
            if not isinstance(a2.parameters[i], Action):
                raise AssertionError("Parameter missmatch")
            if not _same_action(a1.parameters[i], a2.parameters[i]):
                raise AssertionError
        else:
            if a1.parameters[i] != a2.parameters[i]:
                raise AssertionError("Parameter missmatch")
    if a1.to_string() != a2.to_string():
        raise AssertionError
    return True
