#!/bin/bash


#create hadoop user&group
sudo addgroup hadoop
sudo adduser --ingroup hadoop hadoop
#grant superuser privilege by copy file
sudo cp /root/install/sudoers /etc/sudoers