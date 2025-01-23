#!/bin/bash

set -e

prefix="${XDG_DATA_HOME:-$HOME/.local/share}"
krunner_dbusdir="$prefix/krunner/dbusplugins"
services_dir="$prefix/dbus-1/services/"

plugin_dir="$HOME/.local/share/its_mypic"

mkdir -p $plugin_dir
mkdir -p $krunner_dbusdir
mkdir -p $services_dir

cp its_mypic.desktop $krunner_dbusdir
cp -r data main.py database.py clipper $plugin_dir
printf "[D-BUS Service]\nName=org.kde.its_mypic\nExec=\"$plugin_dir/main.py\"" > $services_dir/org.kde.its_mypic.service

kquitapp6 krunner

