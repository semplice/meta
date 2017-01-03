#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# metabuilder: get files ready to be included into the metapackages!
# Copyright (C) 2013 Eugenio "g7" Paolantonio. All rights reserved.
# Work released under the terms of the GNU GPL license, version 3 or
# later.
#

import os, sys, shutil, commands, fileinput

if len(sys.argv) == 1:
	ARCH = commands.getoutput("dpkg-architecture -qDEB_HOST_ARCH")
else:
	ARCH = sys.argv[1]

print("I: metabuilder.py: started")

def base_list(obj):
	""" Creates the base include list. Based on generate.py.
	
	obj is an opened file object. """
	
	ignore_list = (
		"",
		"-",
		"debian-multimedia-keyring",
		"libept0",
		"libept1",
		"libxapian5",
		"liblzma2",
		"libxtables10",

		## FIXME: Due to the systemd transition, we need to blacklist
		## sysvinit, at least for now.
		## systemd-sysv is included in the include list.
		"sysvinit-core",
		"sysvinit-utils",
		"sysv-rc",
	)
	
	# Get package list via aptitude
	package_list = commands.getoutput('aptitude search "~pimportant (?not(?obsolete))" "~prequired (?not(?obsolete))"').split("\n")

	GCC = []
	# Ok, so we have the package_list variable correctly declared.
	# Now we should parse the lines and then the single packages.
	# A 'for' loop really helps.
	for line in package_list:
		col = line.split(" ")
		if col[0] == "c":
			continue
		if col[1] == "A":
			pkg = col[2] + "\n"
		else:
			pkg = col[3] + "\n"

		if pkg.replace("\n","") in ignore_list:
			print("I: base_list(): pkg is %s, skipping." % (pkg))
		elif pkg[:3] == "gcc":
			# GCC packages will be wrote after the loop, the user needs only one gcc, no two or three.
			GCC.append(pkg)
		else:
			obj.write(pkg)
	
	# Write the last package in the 'GCC' list.
	# WARNING: If there is experimental activated, the last gcc version
	# will not be the same present in sid and, therefore, will break system-base.
	# Please run this script only in chroot enviroinment, such as pbuilder.
	# The package *should* automagically create a list of packages. See debian/rules for more details.
	obj.write(GCC[-1])

	obj.close()


# Loop through src/ in search of common package lists...
for item in os.listdir("src/"):
	fullpath = os.path.join("src/", item)
	if os.path.isfile(fullpath):
		# Found one! Process it...
		
		# Check if it has an extension (so it is a one-arch package):
		if len(item.split(".")) > 1:
			# Check arch
			if item.split(".")[-1] != ARCH:
				print("I: skipping %s as we aren't onto the right arch."
					% item)
				continue
		
		print("I: processing %s" % item)
		
		# Firstly, copy the common list to . and change its name
		mainpath = os.path.join(os.getcwd(), "%s-%s" %
			(item.replace(".%s" % ARCH,""), ARCH))
		shutil.copy(fullpath, mainpath)
		
		# Also create a recommends file, otherwise germinate will
		# complain.
		with open(os.path.join(os.getcwd(), "%s-recommends-%s" %
			(item.replace(".%s" % ARCH,""), ARCH)), "w") as f:
				f.write("")
		
		# If this is "base", we need to obtain a list of "required" and
		# "important" packages. To do this, we use a custom method.
		if item.replace(".%s" % ARCH,"") == "base":
			if not os.path.exists("src/%s" % ARCH):
				os.makedirs("src/%s" % ARCH)
			base_list(open("src/%s/base.include" % ARCH, "w"))
		
		# Check in arch dirs if we need to further process this list
		if os.path.isdir("src/%s" % ARCH):
			for architem in os.listdir("src/%s" % ARCH):
				# Check if we are talking about our package
				if ".".join(architem.split(".")[:-1]) == item:
					# Yeah!
					
					# Should exclude?
					if architem.endswith(".exclude"):
						# Get excludes list
						excludes = []
						with open(os.path.join(os.getcwd(), "src/%s/%s" %
							(ARCH, architem))) as f:
							for line in f.readlines():
								excludes.append(line.replace("\n",""))
						
						for line in fileinput.input(mainpath, inplace=1):
							if not line.replace("\n","") in excludes:
								sys.stdout.write(line)
					elif architem.endswith(".include"):
						# Should include!
						
						mainopen = open(mainpath, "a")
						
						with open(os.path.join(os.getcwd(), "src/%s/%s" %
							(ARCH, architem))) as f:
								for line in f.readlines():
									mainopen.write(line)
						
						mainopen.close()

print("I: metabuilder.py: closing...")

