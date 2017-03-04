# -*- coding: utf-8 -*-
"""
Kano is a versioning/archiving tool intended to be a simple solution for version tracking 
for the average user.

Kano provides a simplistic interface where files can be archived by easy to understand
drag and drop operation. Upon dropping a file into the Kano window two further clicks 
archive the file and a human readable text file is generated alongside which contains
a 'version history'. The next time the file is dropped into Kano no further user input
is required.



Kano is released under the GNU General Public License 3.0

Copyright (c) 2017, Michael Schreier
All rights reserved.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui, QtWidgets, QtCore
import Kano_core
import yaml

from const_UI_stylesheets import *

from class_UI_aboutWindow import AboutWindow
from class_UI_settingsWindow import SettingsWindow
from class_UI_NewItemDialog import NewItemDialog
from class_UI_SetArchiveDialog import SetArchiveDialog
from class_UI_toolbar import KanoToolBar
from class_UI_KanoListWidgetItem import KanoListWidgetItem


class KanoUIMain(QtWidgets.QWidget):
	"""
	Main class to house all UI elements, their functions and general program logic
	"""
	def __init__(self):
		super().__init__()

		self.initUI()

		#set up timer to ping queue between this main UI method and worker threads spawned
		#to perform archiving operation
		self.timer = QtCore.QTimer(self)
		self.timer.setInterval(50)
		self.timer.timeout.connect(self.watchdog)
		self.timer.start()
		
		Kano_core.createGlobalRegister()


	def initUI(self):
		#define general window layout and behaviour
		self.setMinimumSize(300,221)
		self.setMaximumSize(300,221)
		self.setWindowTitle('Kano')
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		self.setAcceptDrops(True)
		
		#variable keeping track of whether or not user input is currently required which
		#is used to ensure only one item being worked on at any time
		self.user_input = False
		
		#saving visibility status of each dialog/window used when switching between them
		self.window_state = {
			"ui_main_list": True,
			"ui_new_item_dialog": False,
			"ui_set_archive_dialog": False,
			"ui_about_dialog": False,
			"ui_settings_dialog": False
		}


		#initialize Widgets and Layout
		toolbar = KanoToolBar(self)
		self.ui_main_list = QtWidgets.QListWidget()
		self.ui_new_item_dialog = NewItemDialog()
		self.ui_set_archive_dialog = SetArchiveDialog()
		self.ui_about_dialog = AboutWindow()
		self.ui_settings_dialog = SettingsWindow()

		
		#Qt layout
		self.vboxlayout = QtWidgets.QVBoxLayout()
		self.vboxlayout.setSpacing(0)
		self.setLayout(self.vboxlayout)

		self.vboxlayout.addWidget(toolbar)
		self.vboxlayout.addWidget(self.ui_main_list)
		self.vboxlayout.addWidget(self.ui_new_item_dialog)
		self.vboxlayout.addWidget(self.ui_set_archive_dialog)
		self.vboxlayout.addWidget(self.ui_about_dialog)
		self.vboxlayout.addWidget(self.ui_settings_dialog)

		self.ui_set_archive_dialog.setVisible(False)
		self.ui_new_item_dialog.setVisible(False)
		self.ui_about_dialog.setVisible(False)
		self.ui_settings_dialog.setVisible(False)
		
		
		#more UI settings
		self.ui_main_list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
		self.ui_main_list.verticalScrollBar().setSingleStep(6)
		self.ui_main_list.setAcceptDrops(True)
		self.ui_main_list.setIconSize(QtCore.QSize(16, 16))
		self.ui_main_list.setFrameStyle(QtWidgets.QFrame.NoFrame)
		self.ui_main_list.setStyleSheet(STYLE_ITEM_LIST)
		self.ui_main_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setStyleSheet(STYLE_MAIN_WINDOW)
		
		
		#button behavior
		#--dialog for new items dropped onto Kano
		self.ui_new_item_dialog.button_create_new_archive.clicked.connect(
			lambda: self.toggleSetArchiveDialog(True)
		)
		self.ui_new_item_dialog.button_cancel.clicked.connect(
			lambda: self.toggleNewItemDialog(False)
		)	
		self.ui_new_item_dialog.button_choose_existing_archive.clicked.connect(
			lambda: self.fileDialog(
				self.ui_new_item_dialog, 
				"file", 
				"Open Journal File", 
				"Kano Journals (*.kano.txt)"
			)
		)
		
		#--dialog to choose where to archive files
		self.ui_set_archive_dialog.button_select_archive_path.clicked.connect(
			lambda: self.fileDialog(
				self.ui_set_archive_dialog, 
				"directory", 
				"Open Directory", 
				QtWidgets.QFileDialog.ShowDirsOnly
			)
		)
		self.ui_set_archive_dialog.button_cancel.clicked.connect(
			lambda: self.toggleSetArchiveDialog(False)
		)
		self.ui_set_archive_dialog.button_create_archive.clicked.connect(
			lambda: self.returnToMainView(self.ui_set_archive_dialog)
		)
		self.ui_set_archive_dialog.input_archive_name.textChanged.connect(
			lambda: self.ui_set_archive_dialog.updateArchive()
		)
		self.ui_set_archive_dialog.input_archive_directory.textChanged.connect(
			lambda: self.ui_set_archive_dialog.updateArchive()
		)
		
		#--settings window
		self.ui_settings_dialog.checkbox_fuzzy_matching.clicked.connect(
			lambda: self.updateSettings()
		)
		self.ui_settings_dialog.spinbox_fuzzy_matching_treshold.valueChanged.connect(
			lambda: self.updateSettings()
		)
		self.ui_settings_dialog.checkbox_global_register.clicked.connect(
			lambda: self.updateSettings()
		)
		self.ui_settings_dialog.spinbox_register_length.valueChanged.connect(
			lambda: self.updateSettings()
		)
		self.ui_settings_dialog.button_clear_global_register.clicked.connect(
			lambda: Kano_core.clearGlobalRegister()
		)
		self.ui_settings_dialog.checkbox_zip_files.clicked.connect(
			lambda: self.updateSettings()
		)
		
		#handling of application settings
		#--define default values
		self.settings = {
			'enable_fuzzy_matching': False,
			'fuzzy_matching_treshold': 70,
			'enable_global_register': True,
			'global_register_length': 100,
			'zip_files': False
		}
		
		#--load exisiting settings on startup
		if getattr(sys, 'frozen', False):
			application_path = os.path.dirname(sys.executable)
		elif __file__:
			application_path = os.path.dirname(os.path.realpath(__file__))
		self.settings_file = application_path + "\\settings.cfg"
		if os.path.isfile(self.settings_file):
			with open(self.settings_file, 'r') as file:
				tmp = yaml.load(file)
				#cheap consistency check here
				if 'enable_fuzzy_matching' in tmp:
					self.settings = tmp
		
		if self.settings['enable_fuzzy_matching']:
			tmp = 2
		else:
			tmp = 0
		self.ui_settings_dialog.checkbox_fuzzy_matching.setChecked(
			QtCore.Qt.CheckState(tmp)
		)
		self.ui_settings_dialog.spinbox_fuzzy_matching_treshold.setValue(
			self.settings['fuzzy_matching_treshold']
		)
		if self.settings['enable_global_register']:
			tmp = 2
		else:
			tmp = 0
		self.ui_settings_dialog.checkbox_global_register.setChecked(
			QtCore.Qt.CheckState(tmp)
		)
		self.ui_settings_dialog.spinbox_register_length.setValue(
			self.settings['global_register_length']
		)
		if self.settings['zip_files']:
			tmp = 2
		else:
			tmp = 0
		self.ui_settings_dialog.checkbox_zip_files.setChecked(
			QtCore.Qt.CheckState(tmp)
		)
		
		#toolbar styling and button behaviour
		#--styling/behaviour
		toolbar_action_quit = QtWidgets.QAction(QtGui.QIcon('img/close.png'), 'Exit', self)
		toolbar_action_quit.setShortcut('Ctrl+Q')
		toolbar_action_quit.triggered.connect(self.close)

		toolbar_action_minimize = QtWidgets.QAction(QtGui.QIcon('img/minimize.png'), 'Minimize', self)
		toolbar_action_minimize.setShortcut('Ctrl+M')
		toolbar_action_minimize.triggered.connect(self.minimizeWindow)

		toolbar_action_settings = QtWidgets.QAction(QtGui.QIcon('img/settings.png'), 'Settings', self)
		toolbar_action_settings.setShortcut('Ctrl+S')
		toolbar_action_settings.setCheckable(True)

		toolbar_action_clear = QtWidgets.QAction(QtGui.QIcon('img/erase.png'), 'Clear list', self)
		toolbar_action_clear.setShortcut('Ctrl+D')
		toolbar_action_clear.triggered.connect(self.clearList)
		
		toolbar_action_about = QtWidgets.QAction(QtGui.QIcon('img/about.png'), 'About', self)
		toolbar_action_about.setShortcut('Ctrl+A')
		toolbar_action_about.setCheckable(True)
			
		toolbar_action_pin = QtWidgets.QAction(QtGui.QIcon('img/pin.png'), 'Pin window to front', self)
		toolbar_action_pin.setShortcut('Ctrl+P')
		toolbar_action_pin.setCheckable(True)
		toolbar_action_pin.triggered.connect(lambda: self.pinWindow(toolbar_action_pin.isChecked()))
		
		#--more button behaviour
		toolbar_action_settings.triggered.connect(
			lambda: self.toggleAboutWindow(False)
		)
		toolbar_action_settings.triggered.connect(
			lambda: toolbar_action_about.setChecked(False)
		)
		toolbar_action_settings.triggered.connect(
			lambda: self.toggleSettingsWindow(toolbar_action_settings.isChecked())
		)
		
		toolbar_action_about.triggered.connect(
			lambda: self.toggleSettingsWindow(False)
		)
		toolbar_action_about.triggered.connect(
			lambda: toolbar_action_settings.setChecked(False)
		)
		toolbar_action_about.triggered.connect(
			lambda: self.toggleAboutWindow(toolbar_action_about.isChecked())
		)
		
		#--adding empty, invisible, expanding widget to separate toolbar icons
		empty = QtWidgets.QWidget()
		empty.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

		toolbar.setIconSize(QtCore.QSize(24, 24))
		toolbar.setFloatable(False)
		toolbar.setMovable(False)
		toolbar.addAction(toolbar_action_settings)
		toolbar.addAction(toolbar_action_pin)
		toolbar.addAction(toolbar_action_clear)
		toolbar.addAction(toolbar_action_about)
		toolbar.addWidget(empty)
		toolbar.addAction(toolbar_action_minimize)
		toolbar.addAction(toolbar_action_quit)
		
		self.show()
	
		
	def updateSettings(self):
		"""
		Save current settings to settings file
		"""
		self.settings = {
			'enable_fuzzy_matching': self.ui_settings_dialog.checkbox_fuzzy_matching.isChecked(),
			'fuzzy_matching_treshold': self.ui_settings_dialog.spinbox_fuzzy_matching_treshold.value(),
			'enable_global_register': self.ui_settings_dialog.checkbox_global_register.isChecked(),
			'global_register_length': self.ui_settings_dialog.spinbox_register_length.value(),
			'zip_files': self.ui_settings_dialog.checkbox_zip_files.isChecked()
		}
		with open(self.settings_file, 'w+') as file:
			file.write(yaml.dump(self.settings, default_flow_style=False))
		

	def clearList(self):
		"""
		Clear list of all items that were either archived successfully or where an error
		prevented the operation
		"""
		for row in reversed(range(self.ui_main_list.count())):
			item = self.ui_main_list.item(row)
			if item.status == 'done' or item.status == 'error':
				item = self.ui_main_list.takeItem(row)
				del item
				
	
	def minimizeWindow(self):
		self.setWindowState(QtCore.Qt.WindowMinimized)
	
		
	def pinWindow(self, button_state):
		"""
		Pin window to front.
		Necessary reload of taskbar icon; could potentially be circumvented by falling 
		back on OS internal functions rather than using Qt's own.
		"""
		self.hide()
		if button_state:
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		else:
			self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.show()
		
		
	def fileDialog(self, dialog, type, headline, option):
		"""
		Defines layout and behaviour of file dialogs in Kano
		"""
		if type == "directory":
			file_dialog_return = QtWidgets.QFileDialog.getExistingDirectory(
				self, 
				headline, 
				os.path.dirname(dialog.file_name), 
				option
			)
			if file_dialog_return != "":
				dialog.input_archive_directory.setText(file_dialog_return)
				dialog.journal = (
					file_dialog_return.replace('/', '\\') + 
					'\\' + 
					dialog.input_archive_name.text() + 
					".kano.txt"
				)
		elif type == "file":
			file_dialog_return = QtWidgets.QFileDialog.getOpenFileName(
				self, 
				headline, 
				os.path.dirname(dialog.file_name), 
				option
			)
			if file_dialog_return != ('', ''):
				dialog.journal = file_dialog_return[0]
				self.returnToMainView(dialog)
	
	#-------------------------------------------------------------------------------------
	#methods taking care that switching between dialogs/windows is handled properly
	#handling of window visibility could probably be unified to reduce redundancy
	def toggleAboutWindow(self, button_state):
		if button_state:
			self.window_state["ui_main_list"] = self.ui_main_list.isVisible()
			self.window_state["ui_new_item_dialog"] = self.ui_new_item_dialog.isVisible()
			self.window_state["ui_set_archive_dialog"] = self.ui_set_archive_dialog.isVisible()
			self.window_state["ui_settings_dialog"] = self.ui_settings_dialog.isVisible()
			
			self.ui_main_list.setVisible(False)
			self.ui_new_item_dialog.setVisible(False)
			self.ui_set_archive_dialog.setVisible(False)
			self.ui_settings_dialog.setVisible(False)
			self.ui_about_dialog.setVisible(True)
		else:
			self.ui_main_list.setVisible(self.window_state["ui_main_list"])
			self.ui_new_item_dialog.setVisible(self.window_state["ui_new_item_dialog"])
			self.ui_set_archive_dialog.setVisible(self.window_state["ui_set_archive_dialog"])
			self.ui_settings_dialog.setVisible(self.window_state["ui_settings_dialog"])
			self.ui_about_dialog.setVisible(False)
			
	def toggleSettingsWindow(self, button_state):
		if button_state:
			self.window_state["ui_main_list"] = self.ui_main_list.isVisible()
			self.window_state["ui_new_item_dialog"] = self.ui_new_item_dialog.isVisible()
			self.window_state["ui_set_archive_dialog"] = self.ui_set_archive_dialog.isVisible()
			self.window_state["ui_about_dialog"] = self.ui_about_dialog.isVisible()

			self.ui_main_list.setVisible(False)
			self.ui_new_item_dialog.setVisible(False)
			self.ui_set_archive_dialog.setVisible(False)
			self.ui_about_dialog.setVisible(False)
			self.ui_settings_dialog.setVisible(True)
		else:
			self.ui_main_list.setVisible(self.window_state["ui_main_list"])
			self.ui_new_item_dialog.setVisible(self.window_state["ui_new_item_dialog"])
			self.ui_set_archive_dialog.setVisible(self.window_state["ui_set_archive_dialog"])
			self.ui_about_dialog.setVisible(self.window_state["ui_about_dialog"])
			self.ui_settings_dialog.setVisible(False)

	def toggleNewItemDialog(self, button_state):
		if button_state:
			self.setAcceptDrops(False)
			
			self.window_state["ui_about_dialog"] = self.ui_about_dialog.isVisible()
			self.window_state["ui_settings_dialog"] = self.ui_settings_dialog.isVisible()
			self.window_state["ui_new_item_dialog"] = True

			self.ui_main_list.setMaximumHeight(33)
			self.ui_main_list.setStyleSheet(STYLE_ADJUST_ITEM_LIST)

			for row in range(self.ui_main_list.count()):
				item = self.ui_main_list.item(row)
				if item.uuid != self.ui_new_item_dialog.item_uuid:
					item.setHidden(True)

			self.ui_main_list.setVisible(True)
			self.ui_new_item_dialog.setVisible(True)
			self.ui_about_dialog.setVisible(False)
		else:
			self.setAcceptDrops(True)
			self.ui_main_list.setMaximumHeight(16777215)#default value
			self.ui_main_list.setStyleSheet(STYLE_ITEM_LIST)

			for row in range(self.ui_main_list.count()):
				item = self.ui_main_list.item(row)
				item.setHidden(False)
				if item.uuid == self.ui_new_item_dialog.item_uuid:
					item.setStatus('error', 'aborted by user')

			self.user_input = False

			self.ui_new_item_dialog.setVisible(False)
			self.ui_about_dialog.setVisible(self.window_state["ui_about_dialog"])
			self.ui_settings_dialog.setVisible(self.window_state["ui_settings_dialog"])
			self.window_state["ui_new_item_dialog"] = False

	def toggleSetArchiveDialog(self, button_state):
		if button_state:
			self.ui_set_archive_dialog.item_uuid = self.ui_new_item_dialog.item_uuid
			self.ui_set_archive_dialog.file_name = self.ui_new_item_dialog.file_name
			self.ui_set_archive_dialog.autosetArchiveName()
			self.ui_set_archive_dialog.setLocalArchive()

			self.ui_new_item_dialog.setVisible(False)
			self.ui_set_archive_dialog.setVisible(True)
			
			self.window_state["ui_about_dialog"] = False
			self.window_state["ui_settings_dialog"] = False
			self.window_state["ui_new_item_dialog"] = False
			self.window_state["ui_main_list"] = True
			self.window_state["ui_set_archive_dialog"] = True
		else:
			self.ui_new_item_dialog.setVisible(True)
			self.ui_set_archive_dialog.setVisible(False)
			
			self.window_state["ui_about_dialog"] = False
			self.window_state["ui_settings_dialog"] = False
			self.window_state["ui_new_item_dialog"] = True
			self.window_state["ui_main_list"] = True
			self.window_state["ui_set_archive_dialog"] = False
	
	def returnToMainView(self, dialog):
		self.setAcceptDrops(True)
		self.user_input = False
		self.ui_new_item_dialog.setVisible(False)
		self.ui_set_archive_dialog.setVisible(False)
		self.ui_main_list.setVisible(True)
		self.ui_about_dialog.setVisible(False)
		self.ui_main_list.setMaximumHeight(16777215)#default value
		self.ui_main_list.setStyleSheet(STYLE_ITEM_LIST)
		
		for row in range(self.ui_main_list.count()):
				item = self.ui_main_list.item(row)
				item.setHidden(False)
				if item.uuid == dialog.item_uuid:
					item.queue_to_item.put(dialog.journal)
					
		self.window_state["ui_about_dialog"] = False
		self.window_state["ui_settings_dialog"] = False
		self.window_state["ui_new_item_dialog"] = False
		self.window_state["ui_main_list"] = True
		self.window_state["ui_set_archive_dialog"] = False
	#-------------------------------------------------------------------------------------
	
	def sendToItem(self, uuid, content):
		for row in self.ui_main_list.count():
			item = self.ui_main_list.item(row)
			if item.uuid == uuid:
				item.queue_to_item.put(content)

				
	def createItem(self, name):
		tmp_item = KanoListWidgetItem(path=name)
		self.ui_main_list.addItem(tmp_item)
	
	#-------------------------------------------------------------------------------------	
	#reimplementation of drag & drop behaviour for Kano
	def dragEnterEvent(self, event):
		super().dragEnterEvent(event)
		if event.mimeData().hasUrls():
			event.acceptProposedAction()

	def dropEvent(self, event):
		super().dropEvent(event)
		urls = event.mimeData().text().split('\n')
		for u in urls:
			if u[:8] == 'file:///' and os.path.isfile(u[8:]):
				self.createItem(u[8:].replace("/", "\\"))
	#-------------------------------------------------------------------------------------

	def watchdog(self):
		"""
		check items and associated queues and trigger actions when required
		"""
		for row in range(self.ui_main_list.count()):
			item = self.ui_main_list.item(row)
			if not item.queue_from_item.empty() and self.user_input == False:
				msgin = item.queue_from_item.get(timeout=0)
				item.queue_from_item.task_done()

				if msgin == 'journal not found':
					item.setStatus('user input required')
					self.ui_new_item_dialog.item_uuid = item.uuid
					self.ui_new_item_dialog.file_name = item.path
					self.toggleNewItemDialog(True)
					self.user_input = True
				if msgin == 'done':
					item.setStatus('done')
				if msgin == 'error':
					item.setStatus('error')
				if msgin == 'archive locked':
					item.setStatus('archive locked')
				if msgin == 'processing file':
					item.setStatus('processing file')
			if item.status == 'waiting':
				item.runCopy(self.settings)
				item.setStatus('processing file')

def main():
	app = QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('img/archive.png'))
	ex = KanoUIMain()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
