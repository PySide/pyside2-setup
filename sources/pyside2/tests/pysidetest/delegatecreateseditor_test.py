#!/usr/bin/python

#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the test suite of Qt for Python.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_paths import init_test_paths
init_test_paths(True)

from helper.usesqapplication import UsesQApplication
from testbinding import TestView
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import (QAbstractItemDelegate, QComboBox,
                               QSpinBox, QStyledItemDelegate,
                               QStyleOptionViewItem, QWidget)

id_text = 'This is me'

class DelegateDoesntKeepReferenceToEditor(QAbstractItemDelegate):
    def createEditor(self, parent, option, index):
        comboBox = QComboBox(parent)
        comboBox.addItem(id_text)
        return comboBox


class DelegateKeepsReferenceToEditor(QAbstractItemDelegate):
    def __init__(self, parent=None):
        QAbstractItemDelegate.__init__(self, parent)
        self.comboBox = QComboBox()
        self.comboBox.addItem(id_text)

    def createEditor(self, parent, option, index):
        self.comboBox.setParent(parent)
        return self.comboBox


class EditorCreatedByDelegateTest(UsesQApplication):

    def testDelegateDoesntKeepReferenceToEditor(self):
        view = TestView(None)
        delegate = DelegateDoesntKeepReferenceToEditor()
        view.setItemDelegate(delegate)
        editor = view.getEditorWidgetFromItemDelegate()
        self.assertEqual(type(editor), QComboBox)
        self.assertEqual(editor.count(), 1)
        self.assertEqual(editor.itemData(0, Qt.DisplayRole), id_text)
        editor.metaObject()

    def testDelegateKeepsReferenceToEditor(self):
        view = TestView(None)
        delegate = DelegateKeepsReferenceToEditor()
        view.setItemDelegate(delegate)
        editor = view.getEditorWidgetFromItemDelegate()
        self.assertEqual(type(editor), QComboBox)
        self.assertEqual(editor.count(), 1)
        self.assertEqual(editor.itemData(0, Qt.DisplayRole), id_text)
        editor.metaObject()

    def testIntDelegate(self):
        """PYSIDE-1250: When creating a QVariant, use int instead of long long
           for anything that fits into a int. Verify by checking that a spin
           box is created as item view editor for int."""
        item = QStandardItem()
        item.setData(123123, Qt.EditRole)  # <-- QVariant conversion here
        model = QStandardItemModel()
        model.appendRow(item)
        style_option = QStyleOptionViewItem()
        delegate = QStyledItemDelegate()
        editor = delegate.createEditor(None, style_option, model.index(0, 0))
        self.assertEqual(type(editor), QSpinBox)


if __name__ == '__main__':
    unittest.main()

