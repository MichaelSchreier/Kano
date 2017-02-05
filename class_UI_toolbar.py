# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:46:17 2016

@author: Michael
"""
from PyQt5 import QtWidgets, QtCore

class KanoToolBar(QtWidgets.QToolBar):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.offset = QtCore.QPoint(0, 0)
		self.left_click = False
		
	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		if self.left_click:
			self.parent.move(event.globalPos() - self.offset)
		
	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		if event.button() == QtCore.Qt.LeftButton:
			self.left_click = True
			self.offset = event.pos() + QtCore.QPoint(10, 10)
			#no idea why the offset via QPoint is necessary...
			#as long as the Kano main window was still derived from QMainWindow this was 
			#not neccessary...
			
	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		self.left_click = False