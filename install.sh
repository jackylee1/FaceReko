#!/bin/bash

echo 'Updating and installing dependencies...'
apt-get update && apt-get -y upgrade

apt-get install -y build-essential python-setuptools python-pip awscli

pip install boto3 watchdog simplejson PiCamera
rm -rf ~/.cache/pip

echo 'Configuring AWS...'
aws configure

cd

echo 'Retreving repo files...'
git clone https://github.com/yxkillz/FaceReko.git

echo 'Done!'

exit 0

