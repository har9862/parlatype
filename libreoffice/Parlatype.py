# -*- coding: utf-8 -*-
'''
Parlatype.py is part of Parlatype.
Version: 1.5.6

Copyright (C) Gabor Karsay 2016 <gabor.karsay@gmx.at>

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import dbus


def _getDBUSService():
	try:
		obj = dbus.SessionBus().get_object(
			"com.github.gkarsay.parlatype",
			"/com/github/gkarsay/parlatype")
	except Exception:
		return None
	return dbus.Interface(obj, "com.github.gkarsay.parlatype")


def _getTextRange():
	doc = XSCRIPTCONTEXT.getDocument()

	# the writer controller impl supports
	# the css.view.XSelectionSupplier interface
	xSelectionSupplier = doc.getCurrentController()

	xIndexAccess = xSelectionSupplier.getSelection()
	count = xIndexAccess.getCount()

	# don't mess arount with multiple selections
	if (count != 1):
		return None

	textrange = xIndexAccess.getByIndex(0)

	# don't mess around with selections, just plain cursor
	if (len(textrange.getString()) == 0):
		return textrange
	else:
		return None


def InsertTimestamp():
	textrange = _getTextRange()
	if (textrange is None):
		return

	service = _getDBUSService()
	if (service is None):
		return

	textrange.setString(service.GetTimestamp())


def InsertTimestampOnNewLine():
	textrange = _getTextRange()
	if (textrange is None):
		return

	service = _getDBUSService()
	if (service is None):
		return

	textrange.setString("\n" + service.GetTimestamp() + " ")


def _extractTimestamp():
	textrange = _getTextRange()
	if (textrange is None):
		return None

	xText = textrange.getText()
	cursor = xText.createTextCursorByRange(textrange)

	# select first char on the left
	cursor.goLeft(1, True)

	# we are at beginning of doc
	if (cursor.getString() == ""):
		return None

	i = 0
	while (cursor.getString()[0] != "#" and i < 15):
		cursor.goLeft(1, True)
		i += 1

	# left limit not found
	if (cursor.getString()[0] != "#"):
		return None

	cursor.collapseToStart()

	cursor.goRight(2, True)

	i = 0
	while (cursor.getString()[-1:] != "#" and i < 15):
		cursor.goRight(1, True)
		i += 1

	# right limit not found
	if (cursor.getString()[-1:] != "#"):
		return None

	return cursor.getString()


def GotoTimestamp():
	timestamp = _extractTimestamp()
	if (timestamp is None):
		return

	service = _getDBUSService()
	if (service is None):
		return

	service.GotoTimestamp(timestamp)


def PlayPause():
	service = _getDBUSService()
	if (service is None):
		return

	service.PlayPause()


def JumpBack():
	service = _getDBUSService()
	if (service is None):
		return

	service.JumpBack()


def JumpForward():
	service = _getDBUSService()
	if (service is None):
		return

	service.JumpForward()


def IncreaseSpeed():
	service = _getDBUSService()
	if (service is None):
		return

	service.IncreaseSpeed()


def DecreaseSpeed():
	service = _getDBUSService()
	if (service is None):
		return

	service.DecreaseSpeed()


# Lists the scripts, that shall be visible inside OOo.
# Can be omited, if all functions shall be visible.
g_exportedScripts = \
	InsertTimestamp,\
	InsertTimestampOnNewLine,\
	GotoTimestamp,\
	PlayPause,\
	JumpBack,\
	JumpForward,\
	IncreaseSpeed,\
	DecreaseSpeed,
