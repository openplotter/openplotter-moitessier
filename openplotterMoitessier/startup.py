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

import time, os, subprocess
from openplotterSettings import language


class Start():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-moitessier',currentLanguage)

		self.initialMessage = ''


	def start(self):
		green = '' 
		black = '' 
		red = '' 

		

		time.sleep(2) 
		return {'green': green,'black': black,'red': red}


class Check():
	def __init__(self, conf, currentLanguage):
		self.conf = conf
		currentdir = os.path.dirname(__file__)
		language.Language(currentdir,'openplotter-moitessier',currentLanguage)
		
		self.initialMessage = _('Checking Moitessier HAT...')

	def check(self):
		green = '' 
		black = '' 
		red = '' 

		try:
			out = subprocess.check_output(['more','product'],cwd='/proc/device-tree/hat').decode('utf-8')
		except: black =_('not attached')
		else:
			if not 'Moitessier' in out: black =_('not attached')
			else: green =_('attached')

		try:
			subprocess.check_output(['i2cdetect', '-y', '0']).decode('utf-8')
			red = _('Your Raspberry Pi is too old!')
		except:
			try:
				subprocess.check_output(['i2cdetect', '-y', '1']).decode('utf-8')
				txt = _('I2C enabled')
				if not black: black = txt
				else: black += ' | '+txt
			except:
				txt = _('I2C is disabled. Please enable I2C interface in Preferences -> Raspberry Pi configuration -> Interfaces.')
				if not red: red = txt
				else: red += '\n'+txt

		spidev = subprocess.check_output('lsmod').decode()
		if 'spidev' in spidev:
			txt = _('SPI enabled')
			if not black: black = txt
			else: black += ' | '+txt
		else:
			txt = _('SPI is disabled. Please enable SPI interface in Preferences -> Raspberry Pi configuration -> Interfaces.')
			if not red: red = txt
			else: red += '\n'+txt

		if not os.path.isfile(self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl'):
			txt = _('Moitessier HAT driver is not installed.')
			if not red: red = txt
			else: red += '\n'+txt
		else:
			txt = _('package installed')
			if not black: black = txt
			else: black += ' | '+txt

			package = subprocess.check_output(['dpkg','-s','moitessier']).decode('utf-8')
			kernel = subprocess.check_output(['uname','-r']).decode('utf-8')
			kernel = kernel.split('-')
			kernel = kernel[0]
			package2 = package.split('\n')
			for i in package2:
				if 'Version:' in i:
					version = self.extract_value(i)
					version = version.split('-')
					version = version[2]
			if kernel != version:
				txt = _('The installed package does not match the kernel version, go to OpenPlotter Moitessier HAT app to update it.')
				if not red: red = txt
				else: red += '\n'+txt

		return {'green': green,'black': black,'red': red}

	def extract_value(self, data):
		option, value = data.split(':')
		value = value.strip()
		return value