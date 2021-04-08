#!/bin/bash

# shellcheck disable=SC2005
if [ "$(echo "$(which apt-get)" | wc -l)" -eq 1 ]; then
    sudo apt-get -y install python3-dev gcc
fi

virtualenv -p python3 venv || exit 1
# shellcheck disable=SC1091
source venv/bin/activate
python3 -m pip install -r requirements.txt

#sudo nginx -t || exit 1
#sudo nginx -s reload || exit 1

if [ ! -L "/etc/systemd/system/sambot-formatter.service" ]; then
    sudo ln -s "$(pwd)/sambot-formatter.service" /etc/systemd/system/
fi
sudo systemctl daemon-reload
sudo systemctl restart sambot-formatter.service
sudo systemctl status sambot-formatter.service
