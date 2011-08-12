#!/bin/bash

#
# remove-meta.sh: remove system-<arg> and all its dependencies from the system
# Copyright (C) 2011 Eugenio "g7" Paolantonio and the Semplice Team. All rights reserved.
# The following code is released under the terms of the GNU GPL License, version 3 or later.
#

error() {
	echo "E: $@" 1>&2 
	exit 1
}

warning() {
	echo "W: $@" 1>&2
}

verbose() {
	if [ "$_VERBOSE" ]; then echo "$@"; fi
}

# Parse arguments
for arg in $@; do
	case $arg in
		system-nonfree|system-openbox|system-openbox-base|system-base-graphical)
			# Package.
			pkg="$1"
			;;
		-v|--verbose)
			# Enable verbose output
			_VERBOSE="true"
			;;
		-n|--non-interactive)
			# Enable non-interactive mode
			_NON_INTERACTIVE="true"
			;;
		-f|--force-removal)
			# Forces removal of the packages
			_FORCE="true"
			;;
		-d|--display)
			# Displays the system-nonfree dependencies list.
			_DISPLAY="true"
			;;
		-h|--help)
			# Displays the help
			echo "$0 - Removes <package> and all its dependencies

SYNTAX: $0 <package> [options]

Where package is one of:
 system-nonfree system-openbox system-openbox-base system-base-graphical

Supported options:
 -v|--verbose		Enables verbose output;
 -n|--non-interactive	Noninteractive mode (does not require user intervention);
 -d|--display		Displays <package>'s dependencies;
 -f|--force-removal	Use dpkg (with --force all) to remove packages;
 -h|--help		Displays this message;
"
			exit 0
			;;
	esac
done

if [ -z "$pkg" ]; then
	# pkg not specified or not supported
	error "you must specify a valid package! see  --help for details"
fi

# Require root
verbose "I: Checking privilegies..."
if [ "$UID" != "0" ]; then
	error "You should be root to use $0."
fi

# Check if system-nonfree is installed...
verbose "I: Checking if $pkg is installed..."
output="`dpkg -l $pkg | tail -1`"
if [ -z "$output" ] || [ "`echo $output | awk '{ print $1 }'`" != "ii" ]; then
	# Not installed
	error "$pkg not installed!"
fi

# Now retrieve system-nonfree dependencies
verbose "I: Retrieving $pkg dependencies..."
depends="`dpkg -s $pkg | grep -w \"Depends:\"`"
depends=${depends#"Depends:"} # Remove "Depends:"
depends=${depends//","/""} # Remove all commas

# If we should DISPLAY them, do it now
if [ "$_DISPLAY" ]; then
	verbose "I: Should display them now."
	echo "$pkg dependencies"
	echo "---------------------------"
	echo
	for dep in $depends; do
		echo $dep
	done
	
	echo
	echo "---------------------------"
	
	# Exit
	exit 0
fi

if [ -z "$_FORCE" ]; then
	# Remove system-nonfree and its dependencies from apt
	
	verbose "I: Removing $pkg $depends (via APT)"
	[ "$_NON_INTERACTIVE" ] && _CUSTOPTS="--yes" # Assume yes if non-interactive
	apt-get remove $_CUSTOPTS $pkg $depends
	[ "$?" != "0" ] && error "An error occoured while removing system-nonfree and its dependencies."
else
	# Force mode, remove from dpkg 
	
	verbose "I: Removing $pkg $depends (via dpkg; --force all)"
	dpkg --remove --force all $pkg $depends
	[ "$?" != "0" ] && error "An error occoured while removing system-nonfree and its dependencies."
fi
