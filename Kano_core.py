# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 19:50:11 2016

@author: Michael
"""

import yaml
import shutil
import os
import sys
import getpass
import hashlib
import base64
import datetime
import zlib
import zipfile
from uuid import getnode as get_mac
from fuzzywuzzy import process as get_best_match
from collections import OrderedDict


def initializeJournal(name):
	"""
	create blank journal file
	"""
	directory = os.path.dirname(name)
	if not os.path.exists(directory):
		os.makedirs(directory)
	if not os.path.exists(name):
		open(name, 'a').close()
	
def updateJournal(journal, entry):
	"""
	adds 'entry' to journal
	"""
	with open(journal, 'r') as file:
		content = [c for c in yaml.load_all(file)]
	with open(journal, 'w+') as file:
		content.insert(0, entry)
		file.write(yaml.dump_all(content, default_flow_style=False))


def createJournalEntry(
	checksum=None, 
	comment=None, 
	uid=None, 
	date=None, 
	size=None, 
	original_name=None
):
	"""
	returns formatted journal entry
	"""
	return dict([
		('Checksum', str(checksum)), 
		('Comment', str(comment)), 
		('User ID', str(uid)), 
		('Date', str(date)),
		('Size', str(size) + ' Bytes'),
		('Original file name', str(original_name))
	])
	
	
def createLockFile(file, duration=10):
	"""
	creates a text file with a date 'duration' in the future to prevent other instances
	of Kano to try to write to the same journal file
	"""
	lockfile = file + '.lock'
	with open(lockfile, 'w+') as lfile:
		now = datetime.datetime.utcnow()
		locktime = now + datetime.timedelta(seconds=duration)
		lfile.write(locktime.strftime("%Y-%m-%d %H:%M:%S"))
		return lockfile

def checkLockFile(file):
	"""
	checks for the existence of a lock file and the validity of the timestamp therein
	"""
	lockfile = file + '.lock'
	if os.path.exists(lockfile):
		with open(lockfile, 'r') as f:
			lock = datetime.datetime.strptime(str(f.read()), "%Y-%m-%d %H:%M:%S")
			if (datetime.datetime.utcnow() - lock).total_seconds() <= 0:
				return True
			else:
				return False
	else:
		return False
		

def getUID(length = 6):
	"""
	generates a user ID from the devices MAC-address and OS-username
	"""
	mac = get_mac()
	user = getpass.getuser()
	h = hashlib.sha256()
	type(bytes)
	h.update(str.encode(str(mac) + str(user)))
	uid_hash = h.digest()
	return base64.urlsafe_b64encode(uid_hash).decode('utf-8')[:length]
	

def checksum(file_name, algorithm='sha256'):
	"""
	returns the hash of the input_file
	"""
	if algorithm == 'sha256':
		hash = hashlib.sha256()
		with open(file_name, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash.update(chunk)
		return hash.digest()
	elif algorithm == 'crc32':
		tmp_hash = 0
		with open(file_name, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				tmp_hash = zlib.crc32(chunk, tmp_hash)
		return (tmp_hash & 0xFFFFFFFF)
	else:
		raise NotImplementedError

	
class ChecksumError(Exception):
	"""Raised when checksums do not match"""
	def __init__(self, msg="Checksums of source and copied file do not match"):
		self.msg = msg
		
class MatchError(Exception):
	"""Raised when checksums do not match"""
	def __init__(self, msg="More than one file matched the input file"):
		self.msg = msg
	
								
def uniquename(file_name, time_stamp=None):
	"""
	adds the current date and time to a file name
	"""
	if not time_stamp:
		time_stamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
	base_name, extension = os.path.splitext(file_name)
	return base_name + '_' + time_stamp + extension
	
	
def safecopy(sourcefile, directory, target_name=None, zip_file=False):
	"""
	copies a file, conditionally zips it, and verfies the checksum of the copied file
	"""
	if not os.path.isdir(directory):
		directory = os.path.dirname(directory)
	if not target_name:
		file_name = os.path.basename(sourcefile)
	else:
		file_name = target_name + os.path.splitext(sourcefile)[1]
	archive_name = uniquename(file_name)

	if archive_name in [
		f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
	]:
		raise FileExistsError
	
	archive_path = directory + "\\" + archive_name

	if not zip_file:
		shutil.copy2(sourcefile, archive_path)
		if checksum(archive_path, 'crc32') != checksum(sourcefile, 'crc32'):
			raise ChecksumError
	else:
		archive_path_zip = os.path.splitext(archive_path)[0] + ".zip"
		with zipfile.ZipFile(archive_path_zip, 'w') as zipped_file:
			zipped_file.write(sourcefile, file_name)
		#reopen file and check integrity
		with zipfile.ZipFile(archive_path_zip, 'r') as zipped_file:		
			if zipped_file.testzip() != None:
				raise ChecksumError

		
def createGlobalRegister():
	"""
	creates a text file in the applications's directory to store a history archives
	generated previously
	"""
	if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
	elif __file__:
		application_path = os.path.dirname(os.path.realpath(__file__))
	register = application_path + "\\globalRegister.txt"
	if not os.path.exists(register):
		open(register, 'a').close()

		
def readGlobalRegister():
	"""
	reads the archive history
	"""
	if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
	elif __file__:
		application_path = os.path.dirname(os.path.realpath(__file__))
	register = application_path + "\\globalRegister.txt"
	with open(register, 'r') as f:
		content = f.read().splitlines()
	return content
	
	
def updateGlobalRegister(name=None, max_length=100):
	"""
	adds a new entry to the archive history and truncates the history should it exceed
	the limit given
	"""
	if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
	elif __file__:
		application_path = os.path.dirname(os.path.realpath(__file__))
	register = application_path + "\\globalRegister.txt"
	with open(register, 'r') as f:
		content = f.read().splitlines()
	if name:
		content.insert(0, name)
	content = list(OrderedDict.fromkeys(content))[0:max_length]
	with open(register, 'w+') as f:
		for c in content:
			f.write(c+"\n")
			
			
def clearGlobalRegister():
	"""
	erases all entries in the archive history
	"""
	if getattr(sys, 'frozen', False):
		application_path = os.path.dirname(sys.executable)
	elif __file__:
		application_path = os.path.dirname(os.path.realpath(__file__))
	register = application_path + "\\globalRegister.txt"
	with open(register, 'w+') as f:
		f.write("")

	
def findName(file_path, fuzzy_matching=False, check_global_register=True, treshold=70):
	"""
	given a file (file_path) this method checks for exisiting journals that match the file
	name and returns the best match above the treshold value
	"""
	file = os.path.basename(file_path)
	file_name, extension = os.path.splitext(file)
	directory = os.path.dirname(file_path) + "\\archive"

	#local files first
	names = matches = []
	if os.path.exists(directory):
		names.extend([directory + "\\" + f for f in os.listdir(directory)])
		names = list(filter(lambda x:x.endswith(extension + ".kano.txt"), names))
	if len(names) > 0:
		if fuzzy_matching:
			matches = get_best_match.extract(
				file_name, 
				names, 
				processor=lambda x:os.path.splitext(
					os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0]
				)[0]#take only name of file
			)
		else:
			matches = [
				[m, 100] for m in names if os.path.splitext(
					os.path.splitext(os.path.splitext(os.path.basename(m))[0])[0]
				)[0] == file_name
			]
			matches.append(["", 0])#add zero element
		max_match = matches[0][1]
		matches = [m for m in matches if m[1] == max_match and m[1] >= treshold]
		if len(matches) == 1:
			return matches[0][0]
	
	#then conditionally consider global files
	if check_global_register:
		names = readGlobalRegister()#full path
		if len(names) > 0:
			if fuzzy_matching:
				matches.extend(get_best_match.extract(
					file_name, 
					names, 
					processor=lambda x:os.path.splitext(
						os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0]
					)[0]
				))
			else:
				matches = [
					[m, 100] for m in names if os.path.splitext(
						os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0]
					)[0] == file_name
				]
				matches.append(["", 0])#add zero element
			max_match = max([m[1] for m in matches])
			matches = [m for m in matches if m[1] == max_match and m[1] >= treshold]
			if len(matches) == 1:
				return matches[0][0]
		
		#if len(matches) > 1:
		#		raise MatchError
	else:
		return None