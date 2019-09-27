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
import os, shutil, subprocess
from openplotterSettings import conf
from openplotterSettings import language

def main():
	conf2 = conf.Conf()
	currentdir = os.path.dirname(__file__)
	currentLanguage = conf2.get('GENERAL', 'lang')
	language.Language(currentdir,'openplotter-moitessier',currentLanguage)


	print(_('Copying driver packages...'))
	try:
		confFolder = conf2.conf_folder+'/moitessier'
		if not os.path.exists(confFolder): os.mkdir(confFolder)

		packageFolder = currentdir+'/packages'
		if os.path.exists(packageFolder):
			tmp = os.listdir(packageFolder)
			for i in tmp:
				shutil.copy(packageFolder+'/'+i, confFolder)

		subprocess.call(['chown', '-R', conf2.user, confFolder])

		print(_('DONE'))
	except Exception as e: print(_('FAILED: ')+str(e))


if __name__ == '__main__':
	main()