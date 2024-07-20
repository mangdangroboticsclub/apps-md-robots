#!/usr/bin/bash
set -x

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt-get install python3-pyaudio
sudo apt-get install -y libgl1-mesa-glx
sudo pip install -r $BASEDIR/requirements.txt
