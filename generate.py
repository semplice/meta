#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# script to generate base-$ARCH, using aptitude to get required and important priority packages.
# Maybe is not really clean and cool, maybe should be ran in a chroot enviroinment, but hey, works!
# (C) 2010 Eugenio (g7) <morarossa@gmail.com> - All rights reserved.
# Work released under the GNU GPL license, version 3 or later.
#

# The maintainer should ENSURE that:
# 	- This script is running in a chroot enviroinment, with only Debian and Semplice repositories (a pbuilder hook should do the trick);
#	- In the build enviroinment python and aptitude are installed;
#	- There are NO experimental repositories (nor snapshot repositories).
# Otherwise, system-base can result broken.

#ARCHS = ["i386"]

import os, commands

ignore_list = ("debian-multimedia-keyring", "libept0", "libept1", "libxapian5", "liblzma2")

path = os.getenv('PWD')
if path == None: # needed for debian/rules
	path = "."

ARCHS = [commands.getoutput("dpkg-architecture -qDEB_HOST_ARCH")]

print "I: started generate.py - pwd is %s" % (path)

# Get package list via aptitude
package_list = commands.getoutput('aptitude search "~pimportant (?not(?obsolete))" "~prequired (?not(?obsolete))"').split("\n")

for ARCH in ARCHS: # Now useless starting from 0.6 - to be changed later.
	file = open(path + "/base-" + ARCH,"w")

	GCC = []
	# Ok, so we have the package_list variable correctly declared. Now we should parse the lines and then the single packages. A 'for' loop really helps.
	for line in package_list:
		col = line.split(" ")
		if col[0] == "c":
			continue
		if col[1] == "A":
			pkg = col[2] + "\n"
		else:
			pkg = col[3] + "\n"

		if pkg.replace("\n","") in ignore_list:
			print "pkg is %s, skipping." % (pkg)
		elif pkg[:3] == "gcc":
			# GCC packages will be wrote after the loop, the user needs only one gcc, no two or three.
			GCC.append(pkg)
		else:
			file.write(pkg)
	
	# Write the last package in the 'GCC' list. WARNING: If there is experimental activated, the last gcc version will not the same present in sid and, therefore, will break system-base.
	# Please run this script only in chroot enviroinment, such as pbuilder. The package *should* automagically create a list of packages. See debian/rules for more details.
	file.write(GCC[-1])

	#file.write("!gawk" + "\n")
	#file.write("mawk" + "\n")
	
	# Architecture-dependent packages
	if ARCH in ("i386", "amd64"):
		file.write("""grub-pc
""")
	
	file.write("""sudo
lsb-release
coreutils
binutils
bash-completion
less
bzip2
zip
unzip
tar
gzip
p7zip
unrar-free
console-setup
firmware-linux-free
os-prober
pciutils
usbutils
semplice-apt-conf
ssh
locales""" + "\n")
	file.close()

print "I: all done (hopefully)"
