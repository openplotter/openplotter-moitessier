## openplotter-moitessier

OpenPlotter app to manage the Moitessier HAT

### Installing

#### For production

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **production** and just install this app from *OpenPlotter Apps* tab.

#### For development

Install [openplotter-settings](https://github.com/openplotter/openplotter-settings) for **development**.

Clone the repository:

`git clone https://github.com/openplotter/openplotter-moitessier`

Make your changes and create the package:

```
cd openplotter-moitessier
dpkg-buildpackage -b
```

Install the package:

```
cd ..
sudo dpkg -i openplotter-moitessier_x.x.x-xxx_all.deb
```

Run post-installation script:

`sudo moitessierPostInstall`

Run:

`openplotter-moitessier`

Make your changes and repeat package, installation and post-installation steps to test. Pull request your changes to github and we will check and add them to the next version of the [Debian package](https://launchpad.net/~openplotter/+archive/ubuntu/openplotter).

### Documentation

https://openplotter.readthedocs.io

### Support

http://forum.openmarine.net/forumdisplay.php?fid=1
