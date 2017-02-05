# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:58:14 2016

@author: Michael
"""

from PyQt5 import QtWidgets, QtGui
from const_UI_stylesheets import *
import os

class NewItemDialog(QtWidgets.QDialog):#when using QtWidgets.QWidget background remains partially transparent
	def __init__(self, item_uuid=None, file_name=None):
		super().__init__()#do not call parent here or window is a popup
		
		self.setStyleSheet(STYLE_NEW_ITEM_DIALOG)
		
		#class variables
		self.item_uuid = item_uuid
		self.file_name = file_name
		self.journal = None

		#labels and buttons
		self.label_message = QtWidgets.QLabel()
		self.label_message.setText("Archive not found or ambiguous.\nChoose how to archive file:")
		
		self.button_create_new_archive = QtWidgets.QPushButton(self)
		self.button_create_new_archive.setText("create new")
		
		self.button_choose_existing_archive = QtWidgets.QPushButton(self)
		self.button_choose_existing_archive.setText("choose existing")
		
		self.button_cancel = QtWidgets.QPushButton(self)
		self.button_cancel.setText("abort")
		
		#layout
		self.layout = QtWidgets.QGridLayout()
		self.layout.addWidget(self.label_message, 0, 0, 1, 3)
		self.layout.addWidget(self.button_create_new_archive, 1, 0)
		self.layout.addWidget(self.button_choose_existing_archive, 1, 1)
		self.layout.addWidget(self.button_cancel, 1, 2)
		self.setLayout(self.layout)