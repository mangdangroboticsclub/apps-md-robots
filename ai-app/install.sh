#!/usr/bin/bash
set -x

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt-get install -y python3-pyaudio
sudo pip install -r $BASEDIR/requirements.txt

sudo cp ai.service /etc/systemd/system/ai.service
sudo systemctl start ai

