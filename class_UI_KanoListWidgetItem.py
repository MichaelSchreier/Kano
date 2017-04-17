import os
import uuid
import Kano_core
import time
import datetime
import binascii
import platform
import subprocess

from PyQt5 import QtGui, QtWidgets, QtCore
from queue import Queue
from threading import Thread

from const_UI_stylesheets import *

class KanoListWidgetItem(QtWidgets.QWidget):
	"""
	Customized QListWidgetItem housing files droped into Kano and the subsequently spawned 
	worker thread that takes care of the journal keeping and archiving work
	"""
	def __init__(self, parent=None, status='waiting', path=''):
		super().__init__(parent)
		
		#class variables
		self.status = status
		self.path = path
		self.target_journal = ''
		self.queue_from_item = Queue(maxsize=1)
		self.queue_to_item = Queue(maxsize=1)
		self.uuid = uuid.uuid4()
		self.worker_running = False
		self.button_visibility = False
		
		#widget icon
		self.icon = QtWidgets.QLabel()
		self.image_pixmap = QtGui.QPixmap()
		
		#status text
		#--file name
		self.label_file = QtWidgets.QLabel()
		self.label_file.setTextFormat(QtCore.Qt.RichText)
		file_name = os.path.basename(self.path)
		if len(file_name) > 35:
			file_name = file_name[:32] + '...'
		self.label_file.setText("<b>file:</b> " + file_name)
		
		#--file status
		self.label_status = QtWidgets.QLabel()
		self.label_status.setTextFormat(QtCore.Qt.RichText)
		#self.label_status.setText("<b>status:</b> " + self.status)
		
		
		#buttons
		#--jump to target folder
		self.button_target = QtWidgets.QToolButton()
		self.button_target.setIcon(QtGui.QIcon('img/folder.png'))
		self.button_target.setIconSize(QtCore.QSize(16, 16))
		self.button_target.setToolTip("Open target folder")
		self.button_target.setVisible(False)
		self.button_target.isAvailable = False
		
		#--open respective journal
		self.button_journal = QtWidgets.QToolButton()
		self.button_journal.setIcon(QtGui.QIcon('img/journal.png'))
		self.button_journal.setIconSize(QtCore.QSize(16, 16))
		self.button_journal.setToolTip("Open journal")
		self.button_journal.setVisible(False)
		self.button_journal.isAvailable = False
		
		#--remove entry
		self.button_remove = QtWidgets.QToolButton()
		self.button_remove.setIcon(QtGui.QIcon('img/erase_2.png'))
		self.button_remove.setIconSize(QtCore.QSize(16, 16))
		self.button_remove.setToolTip("Remove from list")
		self.button_remove.setVisible(False)
		self.button_remove.isAvailable = True
		
		#--archive file again
		self.button_redo = QtWidgets.QToolButton()
		self.button_redo.setIcon(QtGui.QIcon('img/redo.png'))
		self.button_redo.setIconSize(QtCore.QSize(16, 16))
		self.button_redo.setToolTip("Archive file again")
		self.button_redo.setVisible(False)
		self.button_redo.isAvailable = True
		
		#layout
		self.layout = QtWidgets.QGridLayout()
		self.layout.setVerticalSpacing(0)
		self.layout.setColumnStretch(1, 8)
		self.layout.addWidget(self.icon, 0, 0, 2, 1, QtCore.Qt.AlignVCenter)
		self.layout.addWidget(self.label_file, 0, 1)
		self.layout.addWidget(self.label_status, 1, 1)
		
		self.layout_button_row = QtWidgets.QHBoxLayout()
		self.layout_button_row.addWidget(self.button_target)
		self.layout_button_row.addWidget(self.button_journal)
		self.layout_button_row.addWidget(self.button_remove)
		self.layout_button_row.addWidget(self.button_redo)
		
		self.layout.addLayout(self.layout_button_row, 2, 1, QtCore.Qt.AlignLeft)
		self.layout.setContentsMargins(QtCore.QMargins(2, 2, 2, 2))
		
		self.setLayout(self.layout)

		self.setStatus(status)
		self.updateStatusText()
		
	def setButtonVisibility(self, visibility):
		"""
		Batch sets the visibility status of all buttons in the widget.
		"""
		self.button_target.setVisible(visibility and self.button_target.isAvailable)
		self.button_journal.setVisible(visibility and self.button_journal.isAvailable)
		self.button_remove.setVisible(visibility and self.button_remove.isAvailable)
		self.button_redo.setVisible(visibility and self.button_redo.isAvailable)
		self.button_visibility = visibility
	

	def setStatus(self, status, custom_text=None):
		"""
		Sets widget icon and status text
		"""
		self.status = status
		if status == 'waiting':
			self.image_pixmap.load('img\wait.png')
		elif status == 'done':
			self.image_pixmap.load('img\ok.png')
		elif status == 'error':
			self.image_pixmap.load('img\error.png')
		elif status == 'user input required':
			self.image_pixmap.load('img\warning.png')
		elif status == 'archive locked':
			self.image_pixmap.load('img\lock.png')
		elif status == 'processing file':
			self.image_pixmap.load('img\circle.png')
		
		self.image_pixmap = self.image_pixmap.scaled(16, 16, transformMode=1)
		self.icon.setPixmap(self.image_pixmap)
		
		self.updateStatusText(custom_text)
	
		
	def updateStatusText(self, custom_text=None):
		"""
		Sets item text based on status
		"""
		if custom_text:
			tmp_text = custom_text
		else:
			tmp_text = self.status
		
		self.label_status.setText("<b>status:</b> " + tmp_text)
	
	
	def openTargetFolder(self):
		"""
		Opens the target folder in the OS's file browser 
		"""
		folder = os.path.dirname(self.target_journal)
		if platform.system() == "Windows":
			os.startfile(folder)
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", folder])
		else:
			subprocess.Popen(["xdg-open", folder])
	
	
	def openTargetJournal(self):
		"""
		Opens the target journal file in the default application
		"""
		if platform.system() == "Windows":
			os.startfile(self.target_journal)
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", target_journal])
		else:
			subprocess.Popen(["xdg-open", target_journal])
			
	
	def runCopy(self, settings):
		"""
		Sets up and starts worker thread handling the archiving operation
		"""
		if not self.worker_running:
			self.worker = Thread(
				target = self.kanoCopy, 
				args = (
					self.path, 
					self.queue_to_item, 
					self.queue_from_item, 
					settings
				)
			)
			self.worker.start()
			self.worker_running = True
	
			
	def kanoCopy(self, file, queue_in, queue_out, settings):
		"""
		Worker thread handling the archiving operation
		"""
		run = True
		
		#check for existing archive
		try:
			journal_file = Kano_core.findName(
				file, 
				settings['enable_fuzzy_matching'], 
				settings['enable_global_register'], 
				settings['fuzzy_matching_treshold']
			)
		except(Exception):
			journal_file = None
		
		if not journal_file:
				queue_out.put('journal not found')
		
		#continously check if journal file has been assigend and start archiving file
		#if that is the case
		while run:
			if not journal_file and not queue_in.empty():	
				journal_file = queue_in.get(timeout=0)		
				queue_in.task_done()			
				if journal_file == 'abort':
					run = False
					journal_file = None
			if journal_file:
				try:
					Kano_core.initializeJournal(journal_file)
					if not Kano_core.checkLockFile(journal_file):

						queue_out.put("processing file")

						lockfile = Kano_core.createLockFile(journal_file, 60)

						archive_folder = os.path.splitext(journal_file)[0]
						tmp_filename = os.path.splitext(
							os.path.splitext(
								os.path.basename(journal_file)
							)[0]
						)[0]

						Kano_core.safecopy(
							file, 
							archive_folder, 
							tmp_filename, 
							settings['zip_files']
						)

						tmp_original_name = os.path.splitext(os.path.basename(file))[0]

						Kano_core.updateJournal(
							journal_file,
							Kano_core.createJournalEntry(
								binascii.hexlify(Kano_core.checksum(file)).decode('utf-8').upper(),
								"File has been zipped" if settings['zip_files'] == True else None,
								Kano_core.getUID(),
								#%z returns empty string because the offset is for utcnow 
								#(which has none); so local time has to be used here...
								datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S (UTC)"),
								os.path.getsize(file),
								tmp_original_name
							)
						)
						
						os.remove(lockfile)
						Kano_core.updateGlobalRegister(
							journal_file, 
							settings['global_register_length']
						)
						run = False
						
						#WARNING -- reference to self must be secured by a lock should
						#more threads access these variables in the future
						self.target_journal = journal_file
						self.button_target.isAvailable = True
						self.button_journal.isAvailable = True
						self.setButtonVisibility(self.button_visibility)
						
						queue_out.put("done")
					else:
						queue_out.put("archive locked")
				except Exception as ex:
					queue_out.put("error")
					run = False

			time.sleep(0.1)
		self.worker_running = False