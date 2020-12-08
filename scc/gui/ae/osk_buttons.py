#!/usr/bin/env python2
"""
SC-Controller - Action Editor - OSK Button Component

Binds controller buttons on on on on on... screen keyboard.
Retuses ButtonsComponent, but hides image, so user can't select mouse or gamepad
button.
"""
from __future__ import unicode_literals
from scc.tools import _
from scc.actions import Action
from scc.gui.ae.buttons import ButtonsComponent
from scc.gui.ae import AEComponent

import logging
log = logging.getLogger("AE.Buttons")

__all__ = [ 'OSKButtonsComponent' ]


class OSKButtonsComponent(ButtonsComponent):
	CTXS = Action.AC_OSK
	PRIORITY = 1
	IMAGES = { }
	
	
	def get_button_title(self):
		return _("Key")
	
	
	def load(self):
		if not self.loaded:
			AEComponent.load(self)
			self.builder.get_object("lblClickAnyButton").set_visible(False)
