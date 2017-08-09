# -*- coding: utf-8 -*-
"""
Created on Mon May 08 19:45:00 2017

@author: Michael
"""

from PyQt5 import QtWidgets, QtGui
from const_UI_stylesheets import *
import os

class CloseDialog(QtWidgets.QDialog):#when using QtWidgets.QWidget background remains partially transparent
	def __init__(self):
		super().__init__()#do not call parent here or window is a popup
		
		self.setStyleSheet(STYLE_CLOSE_DIALOG)
		
		#labels and buttons
		self.label_message = QtWidgets.QLabel()
		self.label_message.setText("Not all files in the queue have been archived yet.\n\nDo you want to close Kano anyway?")
			
		self.button_close = QtWidgets.QPushButton(self)
		self.button_close.setText("close")
		
		self.button_cancel = QtWidgets.QPushButton(self)
		self.button_cancel.setText("cancel")
		
		#layout
		self.layout = QtWidgets.QGridLayout()
		self.layout.addWidget(self.label_message, 0, 0, 1, 2)
		self.layout.addWidget(self.button_close, 1, 0)
		self.layout.addWidget(self.button_cancel, 1, 1)
		self.setLayout(self.layout)