# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:58:14 2016

@author: Michael
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from const_UI_stylesheets import *


class SettingsWindow(QtWidgets.QDialog):#when using QtWidgets.QWidget background remains partially transparent
	def __init__(self, itemuuid=None, filename=None):
		super().__init__()#do not call parent here or window is a popup
		
		self.setStyleSheet(STYLE_SETTINGS_WINDOW)
		
		#labels and buttons
		#--setting 1
		self.label_enable_fuzzy_matching = QtWidgets.QLabel()
		self.label_enable_fuzzy_matching.setText("Enable fuzzy matching to identify archive")
		
		self.checkbox_fuzzy_matching = QtWidgets.QCheckBox()
		
		#--setting 2
		self.label_fuzzy_matching_threshold = QtWidgets.QLabel()
		self.label_fuzzy_matching_threshold.setText("Set fuzzy matching treshold (1-100)")
		
		self.spinbox_fuzzy_matching_treshold = QtWidgets.QSpinBox()
		self.spinbox_fuzzy_matching_treshold.setMinimum(1)
		self.spinbox_fuzzy_matching_treshold.setMaximum(100)
		self.spinbox_fuzzy_matching_treshold.setSingleStep(1)
		self.spinbox_fuzzy_matching_treshold.setValue(70)
		
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
		#---------------------------------------------------------------------------------
		
		#layout
		self.layout = QtWidgets.QGridLayout()
		self.layout.addWidget(self.label_enable_fuzzy_matching, 0, 0)
		self.layout.addWidget(self.checkbox_fuzzy_matching, 0, 1)
		self.layout.addWidget(self.label_fuzzy_matching_threshold, 1, 0)
		self.layout.addWidget(self.spinbox_fuzzy_matching_treshold, 1, 1)
		self.layout.addWidget(self.label_use_global_register, 2, 0)
		self.layout.addWidget(self.checkbox_global_register, 2, 1)
		self.layout.addWidget(self.label_register_length, 3, 0)
		self.layout.addWidget(self.spinbox_register_length, 3, 1)
		self.layout.addWidget(self.label_clear_global_register, 4, 0)
		self.layout.addWidget(self.button_clear_global_register, 4, 1)
		self.setLayout(self.layout)