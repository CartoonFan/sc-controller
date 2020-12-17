from scc.parser import ActionParser

parser = ActionParser()


def _parses_as_itself(action):
    """
    Tests if provided action can be converted to string and
    parsed back to same action.
    """
    # Simple
    a_str = action.to_string()
    if parser.restart(a_str).parse().to_string() != a_str:
        raise AssertionError
    # Multiline
    m_str = action.to_string(True)
    if parser.restart(m_str).parse().to_string() != a_str:
        raise AssertionError
    return True


def _parse_compressed(a_str):
    return parser.restart(a_str).parse().compress()
 
