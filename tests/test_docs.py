from scc.actions import Action


class TestDocs(object):
    """
    Tests every glade file in glade/ directory (and subdirectories) for known
    problems that may cause GUI to crash in some environments.

    (one case on one environment so far)
    """

    def test_every_action_has_docs(self):
        """
        Tests if every known Action is documentated in docs/actions.md
        """
        # Read docs first
        actions_md = file("docs/actions.md", "r").read()
        profile_md = file("docs/profile-file.md", "r").read()

        # Do stupid fulltext search, because currently it's simply fast enough
        for command in Action.ALL:
            if command in (None, "None", "exit"):
                # Woo for special cases
                continue
            anchor = '<a name="%s">' % (command,)
            if anchor not in actions_md:
                raise AssertionError(
                    "Action '%s' is not documented in actions.md" % (command,)
                )

        for key in Action.PKEYS:
            anchor = "#### `%s`" % (key,)
            if key not in profile_md:
                raise AssertionError(
                    "Key '%s' is not documented in profile-file.md" % (key,)
                )
