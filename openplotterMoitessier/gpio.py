#!/usr/bin/env python3

# This file is part of Openplotter.
# Copyright (C) 2019 by Sailoog <https://github.com/openplotter/openplotter-moitessier>
#                     
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.
import subprocess, sys

class Gpio:
	def __init__(self,conf):
		self.conf = conf
		self.used = [] # {'app':'xxx', 'id':'xxx', 'physical':'n'}

	def usedGpios(self):
		try:
			out = subprocess.check_output(['more','product'],cwd='/proc/device-tree/hat').decode(sys.stdin.encoding)
		except:pass
		else:
			if 'Moitessier' in out:
				self.used.append({'app':'Moitessier', 'id':'power', 'physical':'1'})
				self.used.append({'app':'Moitessier', 'id':'power', 'physical':'2'})
				self.used.append({'app':'Moitessier', 'id':'Press/temp/heading', 'physical':'3'})
				self.used.append({'app':'Moitessier', 'id':'power', 'physical':'4'})
				self.used.append({'app':'Moitessier', 'id':'Press/temp/heading', 'physical':'5'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'6'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'9'})
				self.used.append({'app':'Moitessier', 'id':'output', 'physical':'11'})
				self.used.append({'app':'Moitessier', 'id':'output', 'physical':'12'})
				self.used.append({'app':'Moitessier', 'id':'input', 'physical':'13'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'14'})
				self.used.append({'app':'Moitessier', 'id':'output', 'physical':'15'})
				self.used.append({'app':'Moitessier', 'id':'input', 'physical':'16'})
				self.used.append({'app':'Moitessier', 'id':'power', 'physical':'17'})
				self.used.append({'app':'Moitessier', 'id':'output', 'physical':'18'})
				self.used.append({'app':'Moitessier', 'id':'GNSS/AIS', 'physical':'19'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'20'})
				self.used.append({'app':'Moitessier', 'id':'GNSS/AIS', 'physical':'21'})
				self.used.append({'app':'Moitessier', 'id':'GNSS/AIS', 'physical':'23'})
				self.used.append({'app':'Moitessier', 'id':'GNSS/AIS', 'physical':'24'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'25'})
				self.used.append({'app':'Moitessier', 'id':'EEPROM', 'physical':'27'})
				self.used.append({'app':'Moitessier', 'id':'EEPROM', 'physical':'28'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'30'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'34'})
				self.used.append({'app':'Moitessier', 'id':'ground', 'physical':'39'})
		return self.used