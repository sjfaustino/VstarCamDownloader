# VstarCamDownloader
Download video data from a Vstarcam Smart Camera, from the SD Card over a local network.

# Please note
Vstarcam's firmware has been recently updated so whenever the device has booted up it will choose a random port for the web interface to run on. To statically assign a port, please download the program named 'IP Camera Finder' (http://www.eye4.so/download/) and configure the device to use a static IP, this will allow you to choose the necessary port for the web interface to run on, for example port 80.

# Usage

./VstarCamDownloader.py [IP] [PORT] [OUTPUT DIRECTORY] [COPY/MOVE] [USERNAME] [PASSWORD]

e.g. ./VstarCamDownloader.py cameraip.changeip.net 28080 videos/IPCam1 MOVE admin 88888888

# Testing

The program has been tested against a Vstarcam C7837WIP and a C7824WIP, because of the nature of other cameras made by vstarcam, the web interface may be similar in design so the program should work. Other brands of smart cameras such as Foscam are similar, so they may work with this program.
