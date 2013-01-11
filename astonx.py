#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

#    Copyright 2011, 2012 Roderick Bovee
#
#    This file is part of Aston.
#
#    Aston is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Aston is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Aston.  If not, see <http://www.gnu.org/licenses/>.

'''Loads and runs the Aston application.'''
#pylint: disable=C0103

#for compatibility with Python 2
import sip
sip.setapi('QVariant', 2)

# to make some error messages go away
import matplotlib
matplotlib.use('Qt4Agg')

#all the other imports
import sys
import PyQt4
from aston.ui.MainWindow import AstonWindow
qt = PyQt4.QtGui.QApplication(sys.argv)

# translation stuff
import locale
import pkg_resources
try:
    locale.setlocale(locale.LC_ALL, '')
    if locale.getlocale()[0] is not None:
        lang = locale.getlocale()[0]
        tlate = PyQt4.QtCore.QTranslator(qt)
        tlate.load('aston_' + lang + '.qm', \
            pkg_resources.resource_filename('aston', 'i18n'))
        qt.installTranslator(tlate)
except locale.Error:
    pass

# set up the main window and start
aston = AstonWindow()
aston.show()
sys.exit(qt.exec_())