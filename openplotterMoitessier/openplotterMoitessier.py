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

import wx, os, webbrowser, subprocess, ujson
import wx.richtext as rt
import xml.etree.ElementTree as ET
from openplotterSettings import conf
from openplotterSettings import language
from openplotterSettings import platform

class MyFrame(wx.Frame):
	def __init__(self):
		self.conf = conf.Conf()
		self.conf_folder = self.conf.conf_folder
		self.platform = platform.Platform()
		self.currentdir = os.path.dirname(__file__)
		self.currentLanguage = self.conf.get('GENERAL', 'lang')
		self.language = language.Language(self.currentdir,'openplotter-moitessier',self.currentLanguage)
		self.driversFolder = self.conf.conf_folder+'/moitessier'

		wx.Frame.__init__(self, None, title=_('OpenPlotter Moitessier HAT App'), size=(800,444))
		self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
		icon = wx.Icon(self.currentdir+"/data/openplotter-moitessier.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.CreateStatusBar()
		font_statusBar = self.GetStatusBar().GetFont()
		font_statusBar.SetWeight(wx.BOLD)
		self.GetStatusBar().SetFont(font_statusBar)

		self.toolbar1 = wx.ToolBar(self, style=wx.TB_TEXT)
		toolHelp = self.toolbar1.AddTool(101, _('Help'), wx.Bitmap(self.currentdir+"/data/help.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolHelp, toolHelp)
		if not self.platform.isInstalled('openplotter-doc'): self.toolbar1.EnableTool(101,False)
		toolSettings = self.toolbar1.AddTool(102, _('Settings'), wx.Bitmap(self.currentdir+"/data/settings.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolSettings, toolSettings)
		self.toolbar1.AddSeparator()
		toolApply = self.toolbar1.AddTool(104, _('Apply Changes'), wx.Bitmap(self.currentdir+"/data/apply.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolApply, toolApply)
		toolCancel = self.toolbar1.AddTool(105, _('Cancel Changes'), wx.Bitmap(self.currentdir+"/data/cancel.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCancel, toolCancel)

		self.notebook = wx.Notebook(self)
		self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChange)
		self.info = wx.Panel(self.notebook)
		self.drivers = wx.Panel(self.notebook)
		self.settings = wx.Panel(self.notebook)
		self.output = wx.Panel(self.notebook)
		self.notebook.AddPage(self.info, '')
		self.notebook.AddPage(self.drivers, _('Drivers'))
		self.notebook.AddPage(self.settings, _('Settings'))
		self.notebook.AddPage(self.output, '')
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/info.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/driver.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/settings2.png", wx.BITMAP_TYPE_PNG))
		img3 = self.il.Add(wx.Bitmap(self.currentdir+"/data/output.png", wx.BITMAP_TYPE_PNG))
		self.notebook.AssignImageList(self.il)
		self.notebook.SetPageImage(0, img0)
		self.notebook.SetPageImage(1, img1)
		self.notebook.SetPageImage(2, img2)
		self.notebook.SetPageImage(3, img3)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.toolbar1, 0, wx.EXPAND)
		vbox.Add(self.notebook, 1, wx.EXPAND)
		self.SetSizer(vbox)

		self.pageInfo()
		self.pageDrivers()
		self.pageSettings()
		self.pageOutput()

		maxi = self.conf.get('GENERAL', 'maximize')
		if maxi == '1': self.Maximize()
		
		self.Centre()

	def ShowStatusBar(self, w_msg, colour):
		self.GetStatusBar().SetForegroundColour(colour)
		self.SetStatusText(w_msg)

	def ShowStatusBarRED(self, w_msg):
		self.ShowStatusBar(w_msg, (130,0,0))

	def ShowStatusBarGREEN(self, w_msg):
		self.ShowStatusBar(w_msg, (0,130,0))

	def ShowStatusBarBLACK(self, w_msg):
		self.ShowStatusBar(w_msg, wx.BLACK) 

	def ShowStatusBarYELLOW(self, w_msg):
		self.ShowStatusBar(w_msg,(255,140,0)) 

	def onTabChange(self, event):
		self.SetStatusText('')
		if self.notebook.GetSelection() == 2:
			self.toolbar1.EnableTool(104,True)
			self.toolbar1.EnableTool(105,True)
		else:
			self.toolbar1.EnableTool(104,False)
			self.toolbar1.EnableTool(105,False)

	def OnToolHelp(self, event): 
		url = "/usr/share/openplotter-doc/moitessier/moitessier_app.html"
		webbrowser.open(url, new=2)

	def OnToolSettings(self, event): 
		subprocess.call(['pkill', '-f', 'openplotter-settings'])
		subprocess.Popen('openplotter-settings')

	def pageOutput(self):
		self.logger = rt.RichTextCtrl(self.output, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.LC_SORT_ASCENDING)
		self.logger.SetMargins((10,10))

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.logger, 1, wx.EXPAND, 0)
		self.output.SetSizer(sizer)

	def pageInfo(self):
		self.toolbar2 = wx.ToolBar(self.info, style=wx.TB_TEXT)

		toolCheck = self.toolbar2.AddTool(201, _('Check System'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheck, toolCheck)
		toolCheckConf = self.toolbar2.AddTool(205, _('Check configuration'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheckConf, toolCheckConf)
		self.toolbar2.AddSeparator()
		toolInfo = self.toolbar2.AddTool(202, _('Check Settings'), wx.Bitmap(self.currentdir+"/data/settings2.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolInfo, toolInfo)
		self.toolbar2.AddSeparator()
		toolStatistics = self.toolbar2.AddTool(203, _('Statistics'), wx.Bitmap(self.currentdir+"/data/report.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStatistics, toolStatistics)
		toolResetStatistics = self.toolbar2.AddTool(204, _('Reset'), wx.Bitmap(self.currentdir+"/data/refresh.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolResetStatistics, toolResetStatistics)

		self.toolbar3 = wx.ToolBar(self.info, style=wx.TB_TEXT)
		MPU9250 = self.toolbar3.AddTool(301, _('Check IMU temperature'), wx.Bitmap(self.currentdir+"/data/temp.png"))
		self.Bind(wx.EVT_TOOL, self.onMPU9250, MPU9250)
		MS560702BA03 = self.toolbar3.AddTool(302, _('Check pressure'), wx.Bitmap(self.currentdir+"/data/press.png"))
		self.Bind(wx.EVT_TOOL, self.onMS560702BA03, MS560702BA03)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.AddSpacer(10)
		vbox.Add(self.toolbar2, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.AddSpacer(10)
		vbox.Add(self.toolbar3, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.AddStretchSpacer(1)
		self.info.SetSizer(vbox)

	def OnToolCheck(self,e=0):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginBold()
		try:
			out = subprocess.check_output(['more','product'],cwd='/proc/device-tree/hat').decode('utf-8')
		except:
			self.logger.BeginTextColour((130, 0, 0))
			self.logger.WriteText(_('Moitessier HAT is not attached!\n'))
			self.logger.EndTextColour()
		else:
			if not 'Moitessier' in out: 
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('Moitessier HAT is not attached!\n'))
				self.logger.EndTextColour()
			else: 
				self.logger.BeginTextColour((0, 130, 0))
				self.logger.WriteText(_('Moitessier HAT is attached.\n'))
				self.logger.EndTextColour()

		try:
			subprocess.check_output(['i2cdetect', '-y', '0']).decode('utf-8')
			self.logger.BeginTextColour((130, 0, 0))
			self.logger.WriteText(_('Your Raspberry Pi is too old!\n'))
			self.logger.EndTextColour()
		except:
			try:
				subprocess.check_output(['i2cdetect', '-y', '1']).decode('utf-8')
				self.logger.BeginTextColour((0, 130, 0))
				self.logger.WriteText(_('I2C is enabled.\n'))
				self.logger.EndTextColour()
			except:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('I2C is disabled. Please enable I2C interface in Preferences -> Raspberry Pi configuration -> Interfaces.\n'))
				self.logger.EndTextColour()

		spidev = subprocess.check_output('lsmod').decode()
		if 'spidev' in spidev:
			self.logger.BeginTextColour((0, 130, 0))
			self.logger.WriteText(_('SPI is enabled.\n'))
			self.logger.EndTextColour()
		else:
			self.logger.BeginTextColour((130, 0, 0))
			self.logger.WriteText(_('SPI is disabled. Please enable SPI interface in Preferences -> Raspberry Pi configuration -> Interfaces.\n'))
			self.logger.EndTextColour()

		if not os.path.isfile(self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl'):
			self.logger.BeginTextColour((130, 0, 0))
			self.logger.WriteText(_('Moitessier HAT package is not installed!\n'))
			self.logger.EndTextColour()
			self.logger.EndBold()
		else:
			self.logger.BeginTextColour((0, 130, 0))
			self.logger.WriteText(_('Moitessier HAT package is installed.\n'))
			self.logger.EndTextColour()
			package = subprocess.check_output(['dpkg','-s','moitessier']).decode()
			kernel = subprocess.check_output(['uname','-r']).decode()
			kernel = kernel.split('-')
			kernel = kernel[0]
			package2 = package.split('\n')
			for i in package2:
				if 'Version:' in i:
					version = self.extract_value(i)
					version = version.split('-')
					version = version[2]
			if kernel != version:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('The installed package does not match the kernel version, go to "Driver" tab to update it.\n'))
				self.logger.EndTextColour()
			self.logger.EndBold()
			self.logger.BeginTextColour((55, 55, 55))
			self.logger.WriteText(package)
			self.logger.EndTextColour()

	def extract_value(self, data):
		option, value = data.split(':')
		value = value.strip()
		return value

	def OnToolInfo(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('info')
		self.logger.WriteText(output)
		self.logger.EndTextColour()

	def OnToolStatistics(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('stat')
		self.logger.WriteText(output)
		self.logger.EndTextColour()

	def OnToolResetStatistics(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('reset')
		self.logger.WriteText(output)
		self.logger.EndTextColour()

	def onMPU9250(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('mpu')
		self.logger.WriteText(_('MPU-9250 temperature: ')+output)
		self.logger.WriteText(_('To get accurate readings, make sure the sensor is not being read by another application.'))
		self.logger.EndTextColour()

	def onMS560702BA03(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('ms5')
		self.logger.WriteText(_('MS5607-02BA03 pressure and temperature: ')+output)
		self.logger.WriteText(_('To get accurate readings, make sure the sensor is not being read by another application.'))
		self.logger.EndTextColour()

	def on_enable_gnss(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('enable')
		self.logger.WriteText(output)
		self.logger.EndTextColour()

	def on_disable_gnss(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('disable')
		self.logger.WriteText(output)
		self.logger.EndTextColour()

	def on_reset(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('resethat')
		self.logger.WriteText(output)
		self.logger.EndTextColour()

	def getData(self,action):
		if not os.path.isfile(self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl'): return _('Moitessier HAT package is not installed!\n')
		elif action == 'info': return subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','1']).decode()
		elif action == 'stat': return subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','0']).decode()
		elif action == 'reset': return subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','3']).decode()
		elif action == 'mpu': return subprocess.check_output([self.conf.home+'/moitessier/app/sensors/MPU-9250', '/dev/i2c-1']).decode()
		elif action == 'ms5': return subprocess.check_output([self.conf.home+'/moitessier/app/sensors/MS5607-02BA03', '/dev/i2c-1']).decode()
		elif action == 'si7': return subprocess.check_output([self.conf.home+'/moitessier/app/sensors/Si7020-A20', '/dev/i2c-1']).decode()
		elif action == 'enable': return subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','4','1']).decode()
		elif action == 'disable': return subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','4','0']).decode()
		elif action == 'resethat': return subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','2']).decode()

	def pageDrivers(self):
		kernel_box = wx.StaticBox(self.drivers, -1, _(' Current kernel version '))

		kernel_label = wx.StaticText(self.drivers, -1)
		kernel = subprocess.check_output(['uname','-a']).decode('utf-8')
		kernel_label.SetLabel(kernel)

		packages_box = wx.StaticBox(self.drivers, -1, _(' Available packages '))

		self.packages_list = []
		self.packages_select = wx.Choice(self.drivers, choices=self.packages_list, style=wx.CB_READONLY)
		self.readAvailable()

		button_install = wx.Button(self.drivers, label=_('Install'))
		self.Bind(wx.EVT_BUTTON, self.on_install, button_install)

		downloadB = wx.Button(self.drivers, label=_('Download'))
		self.Bind(wx.EVT_BUTTON, self.onDownload, downloadB)

		drivers = wx.Button(self.drivers, label=_('All drivers'))
		self.Bind(wx.EVT_BUTTON, self.onDrivers, drivers)

		v_kernel_box = wx.StaticBoxSizer(kernel_box, wx.VERTICAL)
		v_kernel_box.AddSpacer(5)
		v_kernel_box.Add(kernel_label, 0, wx.ALL | wx.EXPAND, 10)

		h_packages_box = wx.StaticBoxSizer(packages_box, wx.HORIZONTAL)
		h_packages_box.Add(self.packages_select, 1, wx.ALL | wx.EXPAND, 5)
		h_packages_box.Add(button_install, 0, wx.ALL | wx.EXPAND, 5)
		h_packages_box.Add(downloadB, 0, wx.ALL | wx.EXPAND, 5)
		h_packages_box.Add(drivers, 0, wx.ALL | wx.EXPAND, 5)

		update_final = wx.BoxSizer(wx.VERTICAL)
		update_final.Add(v_kernel_box, 0, wx.ALL | wx.EXPAND, 5)
		update_final.Add(h_packages_box, 0, wx.ALL | wx.EXPAND, 5)
		update_final.AddStretchSpacer(1)

		self.drivers.SetSizer(update_final)

	def readAvailable(self):
		self.packages_select.Clear()
		self.packages_list = []
		kernel = subprocess.check_output(['uname','-r']).decode('utf-8')
		kernel = kernel.split('.')
		kernelA = int(kernel[0])
		kernelB = int(kernel[1])
		kernelC = kernel[2].split('-')
		kernelC = int(kernelC[0])
		tmp = os.listdir(self.driversFolder)
		for i in tmp:
			package = i.split('_')
			package = package[1]
			package = package.split('.')
			packageA = int(package[0])
			packageB = int(package[1])
			packageC = int(package[2])
			if packageA >= kernelA:
				if packageB >= kernelB:
					if packageC >= kernelC: self.packages_list.append(i)
		self.packages_select.AppendItems(self.packages_list)
		if len(self.packages_list)>0: self.packages_select.SetSelection(0)

	def on_install(self,e):
		if self.packages_select.GetStringSelection() == '':
			self.ShowStatusBarYELLOW(_('Select a package to install.'))
		else:
			self.ShowStatusBarYELLOW(_('Updating Moitessier Hat modules and firmware...'))
			self.logger.Clear()
			self.notebook.ChangeSelection(3)
			self.logger.EndBold()
			self.logger.BeginTextColour((55, 55, 55))
			command = self.platform.admin+' dpkg -i '+self.driversFolder+'/'+self.packages_select.GetStringSelection()
			popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
			for line in popen.stdout:
				if not 'Warning' in line and not 'WARNING' in line:
					self.logger.WriteText(line)
					self.ShowStatusBarYELLOW(_('Installing package data, please wait... ')+line)
					self.logger.ShowPosition(self.logger.GetLastPosition())
			self.logger.EndTextColour()
			

	def onDownload(self,e):
		kernel = subprocess.check_output(['uname','-r']).decode('utf-8')
		kernel = kernel.split('-')
		kernel = kernel[0]
		file = 'moitessier_'+kernel+'_armhf.deb'
		self.ShowStatusBarYELLOW(_('Searching file ')+file+' ...')
		if os.path.isfile(self.driversFolder+'/'+file):
			self.ShowStatusBarBLACK(_('This file already exists!'))
		else:
			try:
				out = subprocess.check_output(['wget','https://get.rooco.tech/moitessier/buster/release/'+kernel+'/latest/'+file, '-P', self.driversFolder]).decode('utf-8')
				self.ShowStatusBarGREEN(_('File downloaded!'))
			except:
				self.ShowStatusBarRED(_('File not found!'))
		self.readAvailable()

	def onDrivers(self, e):
		url = "https://www.rooco.eu/2018/06/13/firmware-and-drivers-for-raspberry-pi-moitessier-hat/"
		webbrowser.open(url, new=2)

	def pageSettings(self):
		gnss_box = wx.StaticBox(self.settings, -1, ' GNSS ')

		self.button_enable_gnss =wx.Button(self.settings, label= _('Enable'))
		self.Bind(wx.EVT_BUTTON, self.on_enable_gnss, self.button_enable_gnss)

		self.button_disable_gnss =wx.Button(self.settings, label= _('Disable'))
		self.Bind(wx.EVT_BUTTON, self.on_disable_gnss, self.button_disable_gnss)

		general_box = wx.StaticBox(self.settings, -1, _(' General '))

		self.button_reset =wx.Button(self.settings, label= _('Reset HAT'))
		self.Bind(wx.EVT_BUTTON, self.on_reset, self.button_reset)

		self.button_defaults =wx.Button(self.settings, label= _('Load defaults'))
		self.Bind(wx.EVT_BUTTON, self.on_defaults, self.button_defaults)

		ais_box = wx.StaticBox(self.settings, -1, ' AIS ')

		self.simulator = wx.CheckBox(self.settings, label=_('enable simulator'))

		interval_label = wx.StaticText(self.settings, -1, _('interval (ms)'))
		self.interval = wx.SpinCtrl(self.settings, min=1, max=9999, initial=1000)

		mmsi1_label = wx.StaticText(self.settings, -1, _('MMSI boat 1'))
		self.mmsi1 = wx.SpinCtrl(self.settings, min=111111, max=999999999, initial=5551122)

		mmsi2_label = wx.StaticText(self.settings, -1, _('MMSI boat 2'))
		self.mmsi2 = wx.SpinCtrl(self.settings, min=111111, max=999999999, initial=6884120)

		freq1_label = wx.StaticText(self.settings, -1, _('channel A [Hz]'))
		freq2_label = wx.StaticText(self.settings, -1, _('channel B [Hz]'))
		metamask_label = wx.StaticText(self.settings, -1, 'meta data')
		afcRange_label = wx.StaticText(self.settings, -1, 'AFC range [Hz]')

		self.rec1_freq1 = wx.SpinCtrl(self.settings, min=156000000, max=174000000, initial=161975000)
		self.rec1_freq2 = wx.SpinCtrl(self.settings, min=156000000, max=174000000, initial=162025000)
		self.rec1_metamask = wx.Choice(self.settings, choices=(_('none'),'RSSI'), style=wx.CB_READONLY)
		self.rec1_metamask.SetSelection(0)
		self.rec1_afcRange = wx.SpinCtrl(self.settings, min=500, max=2000, initial=1500)

		h_boxSizer2 = wx.StaticBoxSizer(gnss_box, wx.HORIZONTAL)
		h_boxSizer2.AddSpacer(5)
		h_boxSizer2.Add(self.button_enable_gnss, 1, wx.ALL | wx.EXPAND, 5)
		h_boxSizer2.Add(self.button_disable_gnss, 1, wx.ALL | wx.EXPAND, 5)

		h_boxSizer4 = wx.StaticBoxSizer(general_box, wx.HORIZONTAL)
		h_boxSizer4.AddSpacer(5)
		h_boxSizer4.Add(self.button_reset, 1, wx.ALL | wx.EXPAND, 5)
		h_boxSizer4.Add(self.button_defaults, 1, wx.ALL | wx.EXPAND, 5)

		h_boxSizer5 = wx.BoxSizer(wx.HORIZONTAL)
		h_boxSizer5.Add(h_boxSizer2, 1, wx.RIGHT | wx.EXPAND, 10)
		h_boxSizer5.Add(h_boxSizer4, 1, wx.ALL | wx.EXPAND, 0)

		h_boxSizer6 = wx.BoxSizer(wx.HORIZONTAL)
		h_boxSizer6.Add((0,0), 1, wx.LEFT | wx.EXPAND, 5)
		h_boxSizer6.Add(interval_label, 1, wx.LEFT | wx.EXPAND, 5)
		h_boxSizer6.Add(mmsi1_label, 1, wx.LEFT | wx.EXPAND, 5)
		h_boxSizer6.Add(mmsi2_label, 1, wx.LEFT | wx.EXPAND, 5)

		h_boxSizer7 = wx.BoxSizer(wx.HORIZONTAL)
		h_boxSizer7.Add(self.simulator, 1, wx.ALL | wx.EXPAND, 5)
		h_boxSizer7.Add(self.interval, 1, wx.ALL | wx.EXPAND, 5)
		h_boxSizer7.Add(self.mmsi1, 1, wx.ALL | wx.EXPAND, 5)
		h_boxSizer7.Add(self.mmsi2, 1, wx.ALL | wx.EXPAND, 5)

		rec1_labels = wx.BoxSizer(wx.HORIZONTAL)
		rec1_labels.Add(freq1_label, 1, wx.LEFT | wx.EXPAND, 5)
		rec1_labels.Add(freq2_label, 1, wx.LEFT | wx.EXPAND, 5)
		rec1_labels.Add(metamask_label, 1, wx.LEFT | wx.EXPAND, 5)
		rec1_labels.Add(afcRange_label, 1, wx.LEFT | wx.EXPAND, 5)

		receiver1 = wx.BoxSizer(wx.HORIZONTAL)
		receiver1.Add(self.rec1_freq1, 1, wx.ALL | wx.EXPAND, 5)
		receiver1.Add(self.rec1_freq2, 1, wx.ALL | wx.EXPAND, 5)
		receiver1.Add(self.rec1_metamask, 1, wx.ALL | wx.EXPAND, 5)
		receiver1.Add(self.rec1_afcRange, 1, wx.ALL | wx.EXPAND, 5)

		v_boxSizer8 = wx.StaticBoxSizer(ais_box, wx.VERTICAL)
		v_boxSizer8.Add(h_boxSizer6, 0, wx.ALL | wx.EXPAND, 0)
		v_boxSizer8.Add(h_boxSizer7, 0, wx.ALL | wx.EXPAND, 0)
		v_boxSizer8.AddSpacer(15)
		v_boxSizer8.Add(rec1_labels, 0, wx.ALL | wx.EXPAND, 0)
		v_boxSizer8.Add(receiver1, 0, wx.ALL | wx.EXPAND, 0)

		vbox4 = wx.BoxSizer(wx.VERTICAL)
		vbox4.Add(h_boxSizer5, 0, wx.ALL | wx.EXPAND, 5)
		vbox4.Add(v_boxSizer8, 0, wx.ALL | wx.EXPAND, 5)

		self.settings.SetSizer(vbox4)

		self.readSettings()

	def readSettings(self):
		try:
			settings = subprocess.check_output([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','1']).decode('utf-8')
			settings = settings.replace('\t','')
			settings = settings.split('\n')
			for i in settings:
				if 'enabled:' in i:
					if self.extract_value(i) == '1': self.simulator.SetValue(True)
					else: self.simulator.SetValue(False)
				if 'interval:' in i:
					self.interval.SetValue(int(self.extract_value(i)))
				if 'mmsi:' in i:
					data = self.extract_value(i)
					data = data.split(' ')
					self.mmsi1.SetValue(int(data[0])) 
					self.mmsi2.SetValue(int(data[1]))
				if 'channel frequency 1 [Hz]:' in i:
					self.rec1_freq1.SetValue(int(self.extract_value(i)))
				if 'channel frequency 2 [Hz]:' in i:
					self.rec1_freq2.SetValue(int(self.extract_value(i)))
				if 'meta data mask:' in i:
					if self.extract_value(i) == '0x00': self.rec1_metamask.SetSelection(0)
					else: self.rec1_metamask.SetSelection(1)
				if 'afc range [Hz]:' in i and not 'default' in i:
					self.rec1_afcRange.SetValue(int(self.extract_value(i)))
		except:
			self.ShowStatusBarRED(_('Failure reading HAT settings!'))

	def on_defaults(self,e):
		try:
			tree = ET.parse(self.conf.home+'/moitessier/app/moitessier_ctrl/default_config.xml')
			root = tree.getroot()
			for item in root.iter("simulator"):
				for subitem in item.iter("enabled"):
					if subitem.text == '1': self.simulator.SetValue(True)
					else: self.simulator.SetValue(False)
				for subitem in item.iter("interval"):
					self.interval.SetValue(int(subitem.text))
				for subitem in item.iter("mmsi"):
					self.mmsi1.SetValue(int(subitem[0].text)) 
					self.mmsi2.SetValue(int(subitem[1].text))
			for item in root.iterfind('receiver[@name="receiver1"]'):
				for subitem in item.iter("channelFreq"):
					self.rec1_freq1.SetValue(int(subitem[0].text)) 
					self.rec1_freq2.SetValue(int(subitem[1].text))
				for subitem in item.iter("metamask"):
					if subitem.text == '0': self.rec1_metamask.SetSelection(0)
					else: self.rec1_metamask.SetSelection(1)
				for subitem in item.iter("afcRange"):
					self.rec1_afcRange.SetValue(int(subitem.text)) 
		except:
			self.ShowStatusBarRED(_('Failure reading default_config.xml file!'))
		else:
			self.ShowStatusBarBLACK(_('Defaults loaded. Apply changes'))

	def OnToolApply(self,e):
		try: 
			tree = ET.parse(self.conf.home+'/moitessier/app/moitessier_ctrl/config.xml')
			root = tree.getroot()
			for item in root.iter("simulator"):
				for subitem in item.iter("enabled"):
					if self.simulator.GetValue(): subitem.text = '1'
					else: subitem.text = '0'
				for subitem in item.iter("interval"):
					subitem.text = str(self.interval.GetValue())
				for subitem in item.iter("mmsi"):
					subitem[0].text = str(self.mmsi1.GetValue())
					subitem[1].text = str(self.mmsi2.GetValue())
			for item in root.iterfind('receiver[@name="receiver1"]'):
				for subitem in item.iter("channelFreq"):
					subitem[0].text = str(self.rec1_freq1.GetValue())
					subitem[1].text = str(self.rec1_freq2.GetValue())
				for subitem in item.iter("metamask"):
					if self.rec1_metamask.GetSelection() == 0: subitem.text = '0'
					else: subitem.text = '16'
				for subitem in item.iter("afcRange"):
					subitem.text = str(self.rec1_afcRange.GetValue())
			for item in root.iterfind('receiver[@name="receiver2"]'):
				for subitem in item.iter("channelFreq"):
					subitem[0].text = str(self.rec1_freq1.GetValue())
					subitem[1].text = str(self.rec1_freq2.GetValue())
				for subitem in item.iter("metamask"):
					if self.rec1_metamask.GetSelection() == 0: subitem.text = '0'
					else: subitem.text = '16'
				for subitem in item.iter("afcRange"):
					subitem.text = str(self.rec1_afcRange.GetValue())
			tree.write(self.conf.home+'/moitessier/app/moitessier_ctrl/config.xml',encoding='utf-8', xml_declaration=True)
			subprocess.call([self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','5',self.conf.home+'/moitessier/app/moitessier_ctrl/config.xml'])
			self.ShowStatusBarGREEN(_('Changes applied!'))
		except: 
			self.ShowStatusBarRED(_('Apply changes failed!'))

	def OnToolCancel(self,e):
		self.readSettings()

	def OnToolCheckConf(self,e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		self.logger.BeginBold()
		self.logger.WriteText('AIS - GNSS')
		self.logger.EndBold()
		self.logger.Newline()
		if not self.platform.skPort:
			self.logger.EndTextColour()
			self.logger.BeginTextColour((130, 0, 0))
			self.logger.WriteText(_('Please install openplotter-signalk-installer app'))
			self.logger.EndTextColour()
			self.logger.Newline()
		else:
			self.logger.WriteText(_('Connection: '))
			self.logger.EndTextColour()
			connection = ''
			enabled = False
			#check SK
			try:
				setting_file = self.platform.skDir+'/settings.json'
				data = ''
				with open(setting_file) as data_file:
					data = ujson.load(data_file)
				if 'pipedProviders' in data:
					for i in data['pipedProviders']:
						if i['pipeElements'][0]['options']['subOptions']['type']=='serial' and i['pipeElements'][0]['options']['subOptions']['device']=='/dev/moitessier.tty':
							connection = _('Signal K connection ID = ')+i['id']
							enabled = i['enabled']
			except:pass
			#TODO check pypilot-SK, kplex-SK... detect multiple connections
			if connection:
				self.logger.BeginTextColour((0, 130, 0))
				self.logger.WriteText(connection)
				if not enabled:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(' | '+_('disabled'))
			else:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('not connected'))
			self.logger.EndTextColour()
			self.logger.Newline()

		#####################################

			self.logger.BeginTextColour((55, 55, 55))
			self.logger.Newline()
			self.logger.BeginBold()
			self.logger.WriteText(_('Compass - Trim - Heel'))
			self.logger.EndBold()
			self.logger.Newline()
			if not self.platform.isInstalled('openplotter-pypilot'):
				self.logger.EndTextColour()
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('Please install openplotter-pypilot app'))
				self.logger.EndTextColour()
				self.logger.Newline()
			else:
				self.logger.WriteText(_('Pypilot: '))
				self.logger.EndTextColour()
				pypilot = self.conf.get('PYPILOT', 'mode')
				heading = self.conf.get('PYPILOT', 'heading')
				pitch = self.conf.get('PYPILOT', 'pitch')
				roll = self.conf.get('PYPILOT', 'roll')
				pypilotconn2 = self.conf.get('PYPILOT', 'pypilotconn2')
				if pypilot == '1' or pypilot == '2':
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(_('enabled'))
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('disabled'))
				self.logger.EndTextColour()
				self.logger.Newline()
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('Heading: '))
				self.logger.EndTextColour()
				if pypilot != '0' and heading == '1':
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(_('enabled'))
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('disabled'))
				self.logger.EndTextColour()
				self.logger.Newline()
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('Pitch: '))
				self.logger.EndTextColour()
				if pypilot != '0' and pitch == '1':
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(_('enabled'))
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('disabled'))
				self.logger.EndTextColour()
				self.logger.Newline()
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('Roll: '))
				self.logger.EndTextColour()
				if pypilot != '0' and roll == '1':
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(_('enabled'))
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('disabled'))
				self.logger.EndTextColour()
				if pypilot == '1':
					self.logger.BeginTextColour((55, 55, 55))
					self.logger.Newline()
					self.logger.WriteText(_('Connection: '))
					self.logger.EndTextColour()
					connection = ''
					enabled = False
					if self.platform.skPort:
						try:
							setting_file = self.platform.skDir+'/settings.json'
							data = ''
							with open(setting_file) as data_file:
								data = ujson.load(data_file)
							if 'pipedProviders' in data:
								for i in data['pipedProviders']:
									if i['pipeElements'][0]['options']['subOptions']['type']=='udp' and i['pipeElements'][0]['options']['subOptions']['port']==pypilotconn2:
										connection = _('Signal K connection ID = ')+i['id']
										enabled = i['enabled']
						except:pass
					if connection:
						self.logger.BeginTextColour((0, 130, 0))
						self.logger.WriteText(connection)
						if not enabled:
							self.logger.BeginTextColour((130, 0, 0))
							self.logger.WriteText(' | '+_('disabled'))
					else:
						self.logger.BeginTextColour((130, 0, 0))
						self.logger.WriteText(_('not connected'))
					self.logger.EndTextColour()
					self.logger.Newline()
				elif pypilot == '2':
					self.logger.BeginTextColour((55, 55, 55))
					self.logger.Newline()
					self.logger.WriteText(_('Connection 1 (pitch and roll): '))
					self.logger.EndTextColour()
					connection1 = ''
					connection2 = ''
					enabled1 = False
					enabled2 = False
					if self.platform.skPort:
						try:
							setting_file = self.platform.skDir+'/settings.json'
							data = ''
							with open(setting_file) as data_file:
								data = ujson.load(data_file)
							if 'pipedProviders' in data:
								for i in data['pipedProviders']:
									if i['pipeElements'][0]['options']['subOptions']['type']=='udp' and i['pipeElements'][0]['options']['subOptions']['port']==pypilotconn2:
										connection1 = _('Signal K connection ID = ')+i['id']
										enabled1 = i['enabled']
									elif i['pipeElements'][0]['options']['subOptions']['type']=='tcp' and i['pipeElements'][0]['options']['subOptions']['port']=='20220':
										connection2 = _('Signal K connection ID = ')+i['id']
										enabled2 = i['enabled']
						except:pass
					if connection1:
						self.logger.BeginTextColour((0, 130, 0))
						self.logger.WriteText(connection1)
						if not enabled1:
							self.logger.BeginTextColour((130, 0, 0))
							self.logger.WriteText(' | '+_('disabled'))
					else:
						self.logger.BeginTextColour((130, 0, 0))
						self.logger.WriteText(_('not connected'))
					self.logger.EndTextColour()
					self.logger.Newline()
					self.logger.BeginTextColour((55, 55, 55))
					self.logger.WriteText(_('Connection 2 (heading): '))
					self.logger.EndTextColour()
					if connection2:
						self.logger.BeginTextColour((0, 130, 0))
						self.logger.WriteText(connection2)
						if not enabled2:
							self.logger.BeginTextColour((130, 0, 0))
							self.logger.WriteText(' | '+_('disabled'))
					else:
						self.logger.BeginTextColour((130, 0, 0))
						self.logger.WriteText(_('not connected'))
					self.logger.EndTextColour()
					self.logger.Newline()

		###################################

			self.logger.Newline()
			self.logger.BeginTextColour((55, 55, 55))
			self.logger.BeginBold()
			self.logger.WriteText(_('Pressure - Temperature'))
			self.logger.EndBold()
			self.logger.Newline()
			if not self.platform.isInstalled('openplotter-i2c'):
				self.logger.EndTextColour()
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('Please install openplotter-i2c app'))
				self.logger.EndTextColour()
				self.logger.Newline()
			else:
				self.logger.WriteText(_('I2C - Signal K key for pressure: '))
				self.logger.EndTextColour()
				i2c = self.conf.get('I2C', 'sensors')
				i2cconn1 = self.conf.get('I2C', 'i2cconn1')
				try: i2c = eval(i2c)
				except: i2c = {}
				pressure = ''
				temperature = ''
				for sensor in i2c:
					if sensor[0] == 'MS5607-02BA03' and sensor[1] == '0x77':
						pressure = sensor[2][0][0]
						temperature = sensor[2][1][0]
				if pressure:
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(pressure)
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('none'))
				self.logger.EndTextColour()
				self.logger.Newline()
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('I2C - Signal K key for temperature: '))
				self.logger.EndTextColour()
				if temperature:
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(temperature)
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('none'))
				self.logger.EndTextColour()
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.Newline()
				self.logger.WriteText(_('Connection: '))
				self.logger.EndTextColour()
				connection = ''
				enabled = False
				if self.platform.skPort:
					try:
						setting_file = self.platform.skDir+'/settings.json'
						data = ''
						with open(setting_file) as data_file:
							data = ujson.load(data_file)
						if 'pipedProviders' in data:
							for i in data['pipedProviders']:
								if i['pipeElements'][0]['options']['subOptions']['type']=='udp' and i['pipeElements'][0]['options']['subOptions']['port']==i2cconn1:
									connection = _('Signal K connection ID = ')+i['id']
									enabled = i['enabled']
					except:pass
				if connection:
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(connection)
					if not enabled:
						self.logger.BeginTextColour((130, 0, 0))
						self.logger.WriteText(' | '+_('disabled'))
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('not connected'))
				self.logger.EndTextColour()
				self.logger.Newline()

		###################################
		
			self.logger.Newline()
			self.logger.BeginTextColour((55, 55, 55))
			self.logger.BeginBold()
			self.logger.WriteText(_('Signal K to NMEA 0183 conversion'))
			self.logger.EndBold()
			self.logger.Newline()
			self.logger.WriteText(_('Signal K to NMEA 0183 plugin: '))
			self.logger.EndTextColour()
			XDRBaro = False
			XDRNA = False
			HDM = False
			SKplugin = False
			setting_file = self.platform.skDir+'/plugin-config-data/sk-to-nmea0183.json'
			if os.path.isfile(setting_file):
				with open(setting_file) as data_file:
					data = ujson.load(data_file)
				if 'enabled' in data: SKplugin = data['enabled']
				if 'configuration' in data:
					if 'XDRBaro' in data['configuration']: XDRBaro = data['configuration']['XDRBaro']
					if 'XDRNA' in data['configuration']: XDRNA = data['configuration']['XDRNA']
					if 'HDM' in data['configuration']: HDM = data['configuration']['HDM']
			if SKplugin:
				self.logger.BeginTextColour((0, 130, 0))
				self.logger.WriteText(_('enabled'))
			else:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('disabled'))
			self.logger.EndTextColour()
			self.logger.Newline()
			self.logger.BeginTextColour((55, 55, 55))
			self.logger.WriteText(_('XDR (Barometer) conversion: '))
			self.logger.EndTextColour()
			if SKplugin and XDRBaro:
				self.logger.BeginTextColour((0, 130, 0))
				self.logger.WriteText(_('enabled'))
			else:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('disabled'))
			self.logger.EndTextColour()
			self.logger.Newline()
			self.logger.BeginTextColour((55, 55, 55))
			self.logger.WriteText(_('XDR (Pitch and Roll) conversion: '))
			self.logger.EndTextColour()
			if SKplugin and XDRNA:
				self.logger.BeginTextColour((0, 130, 0))
				self.logger.WriteText(_('enabled'))
			else:
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('disabled'))
			self.logger.EndTextColour()
			self.logger.Newline()
			pypilot = self.conf.get('PYPILOT', 'mode')
			if pypilot == '1':
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('HDM (Heading Magnetic) conversion: '))
				self.logger.EndTextColour()
				if SKplugin and HDM:
					self.logger.BeginTextColour((0, 130, 0))
					self.logger.WriteText(_('enabled'))
				else:
					self.logger.BeginTextColour((130, 0, 0))
					self.logger.WriteText(_('disabled'))
				self.logger.EndTextColour()
				self.logger.Newline()
			if pypilot == '2' and SKplugin and HDM:
				self.logger.BeginTextColour((55, 55, 55))
				self.logger.WriteText(_('HDM (Heading Magnetic) conversion: '))
				self.logger.EndTextColour()
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('Duplicated. Please disable HDM conversion'))
				self.logger.EndTextColour()
				self.logger.Newline()


################################################################################

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()
