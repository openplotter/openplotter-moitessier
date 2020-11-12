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

import os, subprocess, sys
from openplotterSettings import language


class Start():
	def __init__(self, conf, currentLanguage):
		self.initialMessage = ''

	def start(self):
		green = '' 
		black = '' 
		red = '' 

		return {'green': green,'black': black,'red': red}


class Check():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(os.path.abspath(__file__))
		language.Language(currentdir,'openplotter-moitessier',currentLanguage)
		
		self.initialMessage = _('Checking Moitessier HAT...')

	def check(self):
		green = '' 
		black = '' 
		red = '' 

		try:
			out = subprocess.check_output(['more','product'],cwd='/proc/device-tree/hat').decode(sys.stdin.encoding)
		except: black =_('not attached')
		else:
			if not 'Moitessier' in out: black =_('not attached')
			else: green =_('attached')

		try:
			out = subprocess.check_output('ls /dev/i2c*', shell=True).decode(sys.stdin.encoding)
			if '/dev/i2c-0' in out: red = _('Your Raspberry Pi is too old!')
			if '/dev/i2c-1' in out:
				txt = _('I2C enabled')
				if not black: black = txt
				else: black += ' | '+txt
		except:
			txt = _('I2C is disabled. Please enable I2C interface in Preferences -> Raspberry Pi configuration -> Interfaces.')
			if not red: red = txt
			else: red += '\n'+txt

		spi_bcm2835 = subprocess.check_output('lsmod').decode(sys.stdin.encoding)
		if 'spi_bcm2835' in spi_bcm2835:
			txt = _('SPI enabled')
			if not black: black = txt
			else: black += ' | '+txt
		else:
			txt = _('SPI is disabled. Please enable SPI interface in Preferences -> Raspberry Pi configuration -> Interfaces.')
			if not red: red = txt
			else: red += '\n'+txt

		modulesPath = self.conf.home+'/moitessier/modules'
		if not os.path.exists(modulesPath):
			txt = _('Moitessier HAT driver is not installed.')
			if not red: red = txt
			else: red += '\n'+txt
		else:
			txt = _('package installed')
			if not black: black = txt
			else: black += ' | '+txt

			packages = os.listdir(modulesPath)
			kernel = subprocess.check_output(['uname','-r']).decode(sys.stdin.encoding)
			kernel = kernel.replace('\n','')
			supported = False
			for i in packages:
				if 'moitessier_'+kernel+'.ko' == i: supported = True
			if not supported:
				txt = _('The installed package does not support the current kernel version, go to Moitessier HAT app to update it.')
				if not red: red = txt
				else: red += '\n'+txt

		return {'green': green,'black': black,'red': red}
