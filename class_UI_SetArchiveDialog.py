# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:58:14 2016

@author: Michael
"""

from PyQt5 import QtWidgets, QtGui
from const_UI_stylesheets import *
import os

class SetArchiveDialog(QtWidgets.QDialog):#when using QtWidgets.QWidget background remains partially transparent
	def __init__(self, item_uuid=None, file_name=None):
		super().__init__()#do not call parent here or window is a popup
		
		self.setStyleSheet(STYLE_SET_ARCHIVE_DIALOG)
		
		#class variables
		self.item_uuid = item_uuid
		self.file_name = file_name
		self.journal = None#set initial value upon opening dialog
		
		#buttons and labels
		self.label_name = QtWidgets.QLabel(self)
		self.label_name.setText("name")
		self.label_dir = QtWidgets.QLabel(self)
		self.label_dir.setText("directory")
		
		self.input_archive_name = QtWidgets.QLineEdit(self)
		self.input_archive_name.setPlaceholderText("archive name")
	
		self.input_archive_directory = QtWidgets.QLineEdit(self)
		self.input_archive_directory.setPlaceholderText("archive directory")
		self.input_archive_directory.setReadOnly(True)
		self.input_archive_directory.setStyleSheet(STYLE_SET_ARCHIVE_LINEEDIT)
		
		self.button_select_archive_path = QtWidgets.QPushButton(self)
		self.button_select_archive_path.setText("select...")
		
		self.button_create_archive = QtWidgets.QPushButton(self)
		self.button_create_archive.setText("create archive")
		
		self.button_cancel = QtWidgets.QPushButton(self)
		self.button_cancel.setText("back")
	
		#Layout
		self.layout = QtWidgets.QGridLayout()
		self.layout.addWidget(self.label_name, 0, 0)
		self.layout.addWidget(self.input_archive_name, 0, 1, 1, 3)
		self.layout.addWidget(self.label_dir, 1, 0)
		self.layout.addWidget(self.input_archive_directory, 1, 1, 1, 2)
		self.layout.addWidget(self.button_select_archive_path, 1, 3)
		self.layout.addWidget(self.button_create_archive, 2, 0, 1, 2)
		self.layout.addWidget(self.button_cancel, 2, 2, 1, 2)
		self.setLayout(self.layout)
		
		
	def autosetArchiveName(self, name=None):
		if name:
			self.input_archive_name.setText(os.path.basename(name))
		elif self.file_name:
			self.input_archive_name.setText(os.path.splitext(os.path.basename(self.file_name))[0])
			
			
	def updateArchive(self):
		self.journal = ( 
			self.input_archive_directory.text() + 
			"\\" + 
			self.input_archive_name.text() + 
			os.path.splitext(self.file_name)[1] + 
			".kano.txt"
		)
			
			
	def setLocalArchive(self):
		if self.file_name:
			self.input_archive_directory.setText(os.path.dirname(self.file_name) + "\\archive")
			
			self.journal = (
				self.input_archive_directory.text() + 
				"\\" + 
				self.input_archive_name.text() + 
				os.path.splitext(self.file_name)[1] + 
				".kano.txt"
			)