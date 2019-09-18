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

import wx, os, webbrowser, subprocess
import wx.richtext as rt
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
		toolCheckConf = self.toolbar1.AddTool(106, _('Check configuration'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheckConf, toolCheckConf)
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
		self.notebook.AddPage(self.info, _('HAT Info'))
		self.notebook.AddPage(self.drivers, _('Drivers'))
		self.notebook.AddPage(self.settings, _('Settings'))
		self.notebook.AddPage(self.output, _('Output'))
		self.il = wx.ImageList(24, 24)
		img0 = self.il.Add(wx.Bitmap(self.currentdir+"/data/openplotter-24.png", wx.BITMAP_TYPE_PNG))
		img1 = self.il.Add(wx.Bitmap(self.currentdir+"/data/openplotter-24.png", wx.BITMAP_TYPE_PNG))
		img2 = self.il.Add(wx.Bitmap(self.currentdir+"/data/openplotter-24.png", wx.BITMAP_TYPE_PNG))
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

		toolCheck = self.toolbar2.AddTool(201, _('Check'), wx.Bitmap(self.currentdir+"/data/check.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolCheck, toolCheck)
		toolInfo = self.toolbar2.AddTool(202, _('Settings'), wx.Bitmap(self.currentdir+"/data/openplotter-24.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolInfo, toolInfo)
		self.toolbar2.AddSeparator()
		toolStatistics = self.toolbar2.AddTool(203, _('Statistics'), wx.Bitmap(self.currentdir+"/data/openplotter-24.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolStatistics, toolStatistics)
		toolResetStatistics = self.toolbar2.AddTool(204, _('Reset'), wx.Bitmap(self.currentdir+"/data/openplotter-24.png"))
		self.Bind(wx.EVT_TOOL, self.OnToolResetStatistics, toolResetStatistics)


		self.toolbar3 = wx.ToolBar(self.info, style=wx.TB_TEXT)
		MPU9250 = self.toolbar3.AddTool(301, _('MPU-9250'), wx.Bitmap(self.currentdir+"/data/openplotter-24.png"))
		self.Bind(wx.EVT_TOOL, self.onMPU9250, MPU9250)
		MS560702BA03 = self.toolbar3.AddTool(302, _('MS5607-02BA03'), wx.Bitmap(self.currentdir+"/data/openplotter-24.png"))
		self.Bind(wx.EVT_TOOL, self.onMS560702BA03, MS560702BA03)
		Si7020A20 = self.toolbar3.AddTool(303, _('Si7020-A20'), wx.Bitmap(self.currentdir+"/data/openplotter-24.png"))
		self.Bind(wx.EVT_TOOL, self.onSi7020A20, Si7020A20)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.AddSpacer(10)
		vbox.Add(self.toolbar2, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.AddSpacer(10)
		vbox.Add(self.toolbar3, 0, wx.LEFT | wx.EXPAND, 0)
		vbox.AddStretchSpacer(1)
		self.info.SetSizer(vbox)

	def OnToolCheck(self,e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginBold()
		try:
			out = subprocess.check_output(['more','product'],cwd='/proc/device-tree/hat').decode()
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

		if not os.path.isfile(self.conf.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl'):
			self.logger.BeginTextColour((130, 0, 0))
			self.logger.WriteText(_('Moitessier HAT package is not installed!\n'))
			self.logger.EndTextColour()
		else:
			self.logger.BeginTextColour((0, 130, 0))
			self.logger.WriteText(_('Moitessier HAT package is installed.\n'))
			self.logger.EndTextColour()
			self.logger.EndBold()
			self.logger.BeginTextColour((55, 55, 55))
			package = subprocess.check_output(['dpkg','-s','moitessier']).decode()
			self.logger.WriteText(package)
			self.logger.EndTextColour()

			kernel = subprocess.check_output(['uname','-r']).decode()
			kernel = kernel.split('-')
			kernel = kernel[0]
			package = package.split('\n')
			for i in package:
				if 'Version:' in i:
					version = self.extract_value(i)
					version = version.split('-')
					version = version[2]
			if kernel != version:
				self.logger.BeginBold()
				self.logger.BeginTextColour((130, 0, 0))
				self.logger.WriteText(_('The installed package does not match the kernel version. Go to "Driver" tab to update the package.'))
				self.logger.EndTextColour()
				self.logger.EndBold()

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

	def onSi7020A20(self, e):
		self.logger.Clear()
		self.notebook.ChangeSelection(3)
		self.logger.BeginTextColour((55, 55, 55))
		output = self.getData('si7')
		if 'Firmware' in output: output = _('This sensor is not mounted on this HAT\n')
		self.logger.WriteText(_('Si7020-A20 humidity: ')+output)
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

		self.rec1_freq1 = wx.SpinCtrl(self.settings, min=159000000, max=162025000, initial=161975000)
		self.rec1_freq2 = wx.SpinCtrl(self.settings, min=159000000, max=162025000, initial=162025000)
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

	def on_defaults(self,e):
		try:
			tree = ET.parse(self.home+'/moitessier/app/moitessier_ctrl/default_config.xml')
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
			self.logger2.Clear()
			self.logger2.BeginTextColour((255, 0, 0))
			self.logger2.WriteText(_('Failure reading default_config.xml file!'))
			self.logger2.EndTextColour()
		else:
			self.logger2.Clear()
			self.logger2.BeginTextColour((55, 55, 55))
			self.logger2.WriteText(_('Defaults loaded. Apply changes.'))
			self.logger2.EndTextColour()

	def OnToolApply(self,e):
		try: 
			tree = ET.parse(self.home+'/moitessier/app/moitessier_ctrl/config.xml')
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
			tree.write(self.home+'/moitessier/app/moitessier_ctrl/config.xml',encoding='utf-8', xml_declaration=True)
			subprocess.call([self.home+'/moitessier/app/moitessier_ctrl/moitessier_ctrl','/dev/moitessier.ctrl','5',self.home+'/moitessier/app/moitessier_ctrl/config.xml'])
			self.logger2.Clear()
			self.logger2.BeginTextColour((55, 55, 55))
			self.logger2.WriteText(_('Changes applied.'))
			self.logger2.EndTextColour()
		except: 
			self.logger2.Clear()
			self.logger2.BeginTextColour((255, 0, 0))
			self.logger2.WriteText(_('Apply changes failed!'))
			self.logger2.EndTextColour()

	def OnToolCancel(self,e):
		pass
		'''
		self.ShowStatusBarRED(_('Changes canceled'))
		self.readMyapp()
		self.readConnections()
		self.printConnections()
		'''

	def OnToolCheckConf(self,e):
		self.conf = Conf()
		self.SK_settings = SK_settings(self.conf)
		self.opencpnSettings = opencpnSettings()
		self.logger4.Clear()

		serialInst = self.conf.get('UDEV', 'Serialinst')
		try: serialInst = eval(serialInst)
		except: serialInst = {}
		serialalias = ''
		assignment = ''
		device = ''
		for alias in serialInst:
			if serialInst[alias]['device'] == '/dev/moitessier.tty' and serialInst[alias]['data'] == 'NMEA 0183': 
				serialalias = alias
				assignment = serialInst[alias]['assignment']
				device = self.SK_settings.check_device(alias)

		pypilot = self.conf.get('PYPILOT', 'mode')
		heading = self.conf.get('PYPILOT', 'translation_magnetic_h')
		attitude = self.conf.get('PYPILOT', 'translation_attitude')

		i2c = self.conf.get('I2C', 'sensors')
		try: i2c = eval(i2c)
		except: i2c = {}
		pressure = ''
		temperature = ''
		for sensor in i2c:
			if sensor[0] == 'MS5607-02BA03' and sensor[1] == '0x77':
				pressure = sensor[2][0][0]
				temperature = sensor[2][1][0]

		XDRBaro = False
		SKplugin = False
		setting_file = self.home+'/.signalk/plugin-config-data/sk-to-nmea0183.json'
		if os.path.isfile(setting_file):
			with open(setting_file) as data_file:
				data = ujson.load(data_file)
			if 'enabled' in data: SKplugin = data['enabled']
			if 'configuration' in data:
				if 'XDRBaro' in data['configuration']: XDRBaro = data['configuration']['XDRBaro']

		opencpnConnection = self.opencpnSettings.getConnectionState()

		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.BeginBold()
		self.logger4.WriteText('AIS - GNSS')
		self.logger4.EndBold()
		self.logger4.Newline()
		self.logger4.WriteText(_('Serial alias: '))
		self.logger4.EndTextColour()
		if serialalias:
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(serialalias)
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('none'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('Assignment: '))
		self.logger4.EndTextColour()
		if not assignment:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('none'))
		elif assignment != 'GPSD':
			if assignment == '0': x = _('manual')
			else: x = assignment
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(x)
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(assignment)
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('Signal K connection status: '))
		self.logger4.EndTextColour()
		if not assignment:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('none'))
		elif assignment == '0' or assignment == 'GPSD' or assignment == 'Signal K > OpenCPN':
			if device == 'enabled':
				self.logger4.BeginTextColour((0, 255, 0))
				self.logger4.WriteText(_('enabled'))
			elif device == 'disabled':
				self.logger4.BeginTextColour((255, 0, 0))
				self.logger4.WriteText(_('disabled'))
			else:
				self.logger4.BeginTextColour((255, 0, 0))
				self.logger4.WriteText(_('connection does not exist'))
		elif 'pypilot' in assignment:
			if self.SK_settings.pypilot_enabled == True:
				self.logger4.BeginTextColour((0, 255, 0))
				self.logger4.WriteText(_('enabled'))
			else:
				self.logger4.BeginTextColour((255, 0, 0))
				self.logger4.WriteText(_('disabled'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('none'))
		self.logger4.EndTextColour()

		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.Newline()
		self.logger4.BeginBold()
		self.logger4.WriteText(_('Compass - Heel - Trim'))
		self.logger4.EndBold()
		self.logger4.Newline()
		self.logger4.WriteText(_('Pypilot status: '))
		self.logger4.EndTextColour()
		if pypilot == 'basic autopilot' or pypilot == 'imu':
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('enabled'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('disabled'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('Heading: '))
		self.logger4.EndTextColour()
		if pypilot != 'disabled' and heading == '1':
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('enabled'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('disabled'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('Pitch, Roll: '))
		self.logger4.EndTextColour()
		if pypilot != 'disabled' and attitude == '1':
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('enabled'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('disabled'))
		self.logger4.EndTextColour()

		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.BeginBold()
		self.logger4.WriteText(_('Pressure - Temperature'))
		self.logger4.EndBold()
		self.logger4.Newline()
		self.logger4.WriteText(_('I2C - Signal K key for pressure: '))
		self.logger4.EndTextColour()
		if pressure:
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(pressure)
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('none'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('I2C - Signal K key for temperature: '))
		self.logger4.EndTextColour()
		if temperature:
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(temperature)
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('none'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('Signal K to NMEA 0183 plugin: '))
		self.logger4.EndTextColour()
		if SKplugin:
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('enabled'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('disabled'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('XDR (Barometer) conversion: '))
		self.logger4.EndTextColour()
		if SKplugin and XDRBaro:
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('enabled'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('disabled'))
		self.logger4.EndTextColour()

		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.BeginBold()
		self.logger4.WriteText(_('OpenCPN'))
		self.logger4.EndBold()
		self.logger4.Newline()
		self.logger4.WriteText(_('Signal K connection: '))
		self.logger4.EndTextColour()
		if opencpnConnection:
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('TCP localhost 10110 input'))
		else:
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('missing TCP localhost 10110 input'))
		self.logger4.EndTextColour()
		self.logger4.Newline()
		self.logger4.BeginTextColour((55, 55, 55))
		self.logger4.WriteText(_('Status: '))
		self.logger4.EndTextColour()
		if not opencpnConnection or opencpnConnection == 'disabled':
			self.logger4.BeginTextColour((255, 0, 0))
			self.logger4.WriteText(_('disabled'))
		if opencpnConnection == 'enabled':
			self.logger4.BeginTextColour((0, 255, 0))
			self.logger4.WriteText(_('enabled'))

################################################################################

def main():
	app = wx.App()
	MyFrame().Show()
	app.MainLoop()

if __name__ == '__main__':
	main()
