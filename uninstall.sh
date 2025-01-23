#!/bin/bash

set -e

prefix="${XDG_DATA_HOME:-$HOME/.local/share}"
krunner_dbusdir="$prefix/krunner/dbusplugins"
plugin_dir="$HOME/.local/share/its_mypic"


rm -r $plugin_dir
rm $prefix/dbus-1/services/org.kde.its_mypic.service
rm $krunner_dbusdir/its_mypic.desktop
kquitapp6 krunner

