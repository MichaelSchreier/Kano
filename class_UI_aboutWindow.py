# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:19:10 2016

@author: Michael
"""
from PyQt5 import QtWidgets

class AboutWindow(QtWidgets.QTextEdit):
	def __init__(self, parent=None):
		super().__init__(parent)
		
		self.setReadOnly(True)
		self.setHtml(
			"""
			<h1 id="kano">Kano</h1>

			<p>Copyright (c) 2017, Michael Schreier <br>
			All rights reserved.</p>
			
			<p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>
			
			<p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>
			
			<p>You should have received a copy of the GNU General Public License along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a></p>
			
			<hr>
			
			<p>Kano has been built using the following libraries:</p>
			
			<h3 id="entypo">Entypo+</h3>
			
			<blockquote>
			  <p>All icons used by Kano are taken unmodified from the “Entypo+” library by Daniel Bruce, available under the Creative Commons license CC BY-SA 4.0.</p>
			</blockquote>
			
			<h3 id="pyqt5">PyQt5</h3>
			
			<blockquote>
			  <p>Copyright (c) 2017, Riverbank Computing Limited <br>
			  All rights reserved.</p>
			  
			  <p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by &gt;the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p>
			  
			  <p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>
			  
			  <p>You should have received a copy of the GNU General Public License along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a></p>
			</blockquote>
			
			
			
			<h3 id="fuzzywuzzy">FuzzyWuzzy</h3>
			
			<blockquote>
			  <p>Copyright (c) 2017, SeatGeak <br>
			  All rights reserved.</p>
			  
			  <p>This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.</p>
			  
			  <p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>
			  
			  <p>You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA</p>
			</blockquote>
			"""
		)