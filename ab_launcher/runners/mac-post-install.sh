#!/bin/sh


### SETTING THE PYTHON EXECUTABLE ICON TO AB

# Sets an icon on file or directory
# Usage setIcon.sh iconimage.jpg /path/to/[file|folder]
iconSource=./assets/activity-browser.icns
iconDestination=./AB/environment/bin/python3.11
icon=/tmp/`basename $iconSource`
rsrc=/tmp/icon.rsrc

# Create icon from the iconSource
cp $iconSource $icon

# Add icon to image file, meaning use itself as the icon
sips -i $icon

# Take that icon and put it into a rsrc file
DeRez -only icns $icon > $rsrc

# Apply the rsrc file to
SetFile -a C $iconDestination

# Destination is a file
Rez -append $rsrc -o $iconDestination

# Remove files that we don't need anymore
rm $rsrc $icon

##
rm -rf ./AB/pkgs