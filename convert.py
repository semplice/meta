#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Convert script for semplice-desktop -> semplice-meta
# Wrote in python because of its great split function.
# (C) 2010 Eugenio (g7) <morarossa@gmail.com> - All rights reserved.
# Work released under the GNU GPL license, version 3 or later.
#

import os

path = os.getenv('PWD')

print "I: started convert.py - pwd is %s" % (path)

# Is not really cool using arguments for this type of operation. Maybe we can use a separate file, but this works the same.
packages = """openbox, volwheel, notify-osd, pcmanfm, fbpanel-legacy, cairo-compmgr, nitrogen, libnotify-bin, laiv-setup, semplice-utilities, semplice-artwork, semplice-default-settings,
         coreutils, binutils, bash-completion, less, grub, semplice-grub-config, semplice-archive-keyring,
         gnome-system-tools, gpe-taskmanager, network-manager-gnome, gnome-disk-utility, synaptic, libtdpkg-1.0-0, menu, lxappearance2-git, lxrandr, xscreensaver, xscreensaver-data,
         gmrun, roxterm, guake, galculator, ristretto, gpaint, xfburn, xarchiver, parcellite, xfce4-screenshooter, mousepad,
         gxine, gmpc, mpd,
         bzip2, zip, unzip, tar, gzip, p7zip, unrar-free,
         chromium-browser, claws-mail, gftp, pidgin,
         abiword, gnumeric, epdfview,
         xserver-xorg, dmz-cursor-theme, libgl1-mesa-dri, libgl1-mesa-glx, x11-xserver-utils, gdm,
         system-config-printer, cups, cups-driver-gutenprint, foomatic-db-gutenprint, foomatic-filters, fontconfig, libtiff4, libfreetype6, hplip,
         firmware-linux-free
"""

# semplice-desktop = desktop-i386, feel free to change the architecture.

if os.path.isfile(path + "/desktop-i386"): # yeah, yeah... using open function in write mode will overwrited the file, and so no need to delete it. But this is cool, babe.
	os.remove(path + "/desktop-i386")

file = open(path + "/desktop-i386","w")
packages = packages.split("\n")

# Ok, so we have the packages variable correctly declared. Now we should parse the lines and then the single packages. A 'for' loop really helps.
for line in packages:
	line = line.replace(" ","") # Remove whitespaces
	line = line.replace("\n","") # Remove newlines
	line = line.split(",")
	for package in line:
		if package == '':
			continue
		file.write(package + "\n")

file.close()

print "I: all done (hopefully)"
