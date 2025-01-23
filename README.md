### its mypic

This plugin provides a quick copy function for a KRunner plugin using dbus.

The install script copies the KRunner config file and a D-Bus activation service file to their appropriate locations.
This way the Python script gets executed when KRunner requests matches and it does not need to be autostarted.

## Installation

```bash
git clone https://github.com/jeffpeng3/krunner-Its-MyPic.git
cd krunner-Its-MyPic
./install.sh
```

## Usage
Alt+Space to open KRunner, type `go` and search for a file, press Enter to copy the file to the clipboard.

![alt text](docs/image.png)