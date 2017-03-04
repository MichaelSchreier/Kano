# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:58:14 2016

@author: Michael
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from const_UI_stylesheets import *


class SettingsWindow(QtWidgets.QScrollArea):#when using QtWidgets.QWidget background remains partially transparent
	def __init__(self, itemuuid=None, filename=None):
		super().__init__()#do not call parent here or window is a popup
		
		self.setStyleSheet(STYLE_SETTINGS_WINDOW)
		
		#scroll area widget
		self.scroll_area_widget = QtWidgets.QDialog()
		self.scroll_area_widget.resize(263, 200)

		#labels and buttons
		#--setting 1
		self.label_enable_fuzzy_matching = QtWidgets.QLabel()
		self.label_enable_fuzzy_matching.setText("Enable fuzzy matching to identify\narchive")
		
		self.checkbox_fuzzy_matching = QtWidgets.QCheckBox()
		
		#--setting 2
		self.label_fuzzy_matching_threshold = QtWidgets.QLabel()
		self.label_fuzzy_matching_threshold.setText("Set fuzzy matching treshold (1-100)")
		
		self.spinbox_fuzzy_matching_treshold = QtWidgets.QSpinBox()
		self.spinbox_fuzzy_matching_treshold.setMinimum(1)
		self.spinbox_fuzzy_matching_treshold.setMaximum(100)
		self.spinbox_fuzzy_matching_treshold.setSingleStep(1)
		self.spinbox_fuzzy_matching_treshold.setValue(70)
		
		#--divider 1
		self.divider_1 = QtWidgets.QFrame()
		self.divider_1.setFrameShape(QtWidgets.QFrame.HLine)
		self.divider_1.setFrameShadow(QtWidgets.QFrame.Sunken)
		
		#--setting 3
		self.label_use_global_register = QtWidgets.QLabel()
		self.label_use_global_register.setText("Search for archives also in previously\nused folders")
		
		self.checkbox_global_register = QtWidgets.QCheckBox()
		self.checkbox_global_register.setCheckState(QtCore.Qt.CheckState(2))
		
		#--setting 4
		self.label_register_length = QtWidgets.QLabel()
		self.label_register_length.setText("Maximum number of folders to track")
		
		self.spinbox_register_length = QtWidgets.QSpinBox()
		self.spinbox_register_length.setMinimum(0)
		self.spinbox_register_length.setMaximum(1000)
		self.spinbox_register_length.setSingleStep(1)
		self.spinbox_register_length.setValue(100)
		
		#--button 1
		self.label_clear_global_register = QtWidgets.QLabel()
		self.label_clear_global_register.setText("Clear folder history")
		
		self.button_clear_global_register = QtWidgets.QPushButton(self)
		self.button_clear_global_register.setText("clear")
		
		#--divider 2
		self.divider_2 = QtWidgets.QFrame()
		self.divider_2.setFrameShape(QtWidgets.QFrame.HLine)
		self.divider_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		
		#--setting 5
		self.label_zip_files = QtWidgets.QLabel()
		self.label_zip_files.setText("Zip archived files")
		
		self.checkbox_zip_files = QtWidgets.QCheckBox()
		self.checkbox_zip_files.setCheckState(QtCore.Qt.CheckState(0))
		#---------------------------------------------------------------------------------
		
		#layout
		self.layout = QtWidgets.QGridLayout()
		self.layout.setContentsMargins(QtCore.QMargins(5, 5, 5, 5))
		self.layout.addWidget(self.label_enable_fuzzy_matching, 0, 0)
		self.layout.addWidget(self.checkbox_fuzzy_matching, 0, 1)
		self.layout.addWidget(self.label_fuzzy_matching_threshold, 1, 0)
		self.layout.addWidget(self.spinbox_fuzzy_matching_treshold, 1, 1)
		
		self.layout.addWidget(self.divider_1, 2, 0, 1, 2)
		
		self.layout.addWidget(self.label_use_global_register, 3, 0)
		self.layout.addWidget(self.checkbox_global_register, 3, 1)
		self.layout.addWidget(self.label_register_length, 4, 0)
		self.layout.addWidget(self.spinbox_register_length, 4, 1)
		self.layout.addWidget(self.label_clear_global_register, 5, 0)
		self.layout.addWidget(self.button_clear_global_register, 5, 1)
		
		self.layout.addWidget(self.divider_2, 6, 0, 1, 2)
		
		self.layout.addWidget(self.label_zip_files, 7, 0)
		self.layout.addWidget(self.checkbox_zip_files, 7, 1)
		self.scroll_area_widget.setLayout(self.layout)
		#---------------------------------------------------------------------------------
		
		#set widget to scroll area
		self.setWidget(self.scroll_area_widget)