import os
import uuid
import Kano_core
import time
import datetime
import binascii

from PyQt5 import QtGui, QtWidgets
from queue import Queue
from threading import Thread

from const_UI_stylesheets import *

class KanoListWidgetItem(QtWidgets.QListWidgetItem):
	"""
	Customized QListWidgetItem housing files droped into Kano and the subsequently spawned 
	worker thread that takes care of the journal keeping and archiving work
	"""
	def __init__(self, status='waiting', path=''):
		super().__init__()
		
		#class variables
		self.status = status
		self.path = path
		self.queue_from_item = Queue(maxsize=1)
		self.queue_to_item = Queue(maxsize=1)
		self.uuid = uuid.uuid4()
		self.worker_running = False

		self.setStatus(status)
		self.updateText()
	

	def setStatus(self, status, custom_text=None):
		"""
		Sets item image
		"""
		self.status = status
		if status == 'waiting':
			self.setIcon(QtGui.QIcon('img\wait.png'))
		elif status == 'done':
			self.setIcon(QtGui.QIcon('img\ok.png'))
		elif status == 'error':
			self.setIcon(QtGui.QIcon('img\error.png'))
		elif status == 'user input required':
			self.setIcon(QtGui.QIcon('img\warning.png'))
		elif status == 'archive locked':
			self.setIcon(QtGui.QIcon('img\lock.png'))
		elif status == 'processing file':
			self.setIcon(QtGui.QIcon('img\circle.png'))
		self.updateText(custom_text)
	
		
	def updateText(self, custom_text=None):
		"""
		Sets item text based on status
		"""
		file = os.path.basename(self.path)
		if len(file) > 40:
			file = file[:37] + '...'
		if custom_text:
			tmp_text = custom_text
		else:
			tmp_text = self.status
		text = file + '\nstatus: ' + tmp_text
		super().setText(text)
	
		
	def runCopy(self, settings):
		"""
		Sets up and starts worker thread handling the archiving operation
		"""
		if not self.worker_running:
			self.worker = Thread(
				target=self.kanoCopy, 
				args=(
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
						queue_out.put("done")
					else:
						queue_out.put("archive locked")
				except (Exception):
					queue_out.put("error")
					run = False

			time.sleep(0.1)