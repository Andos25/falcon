#!/bin/bash

#install R
echo "add an entry for R in /etc/apt/source.list"
sudo echo "deb http://ftp.ctex.org/mirrors/CRAN/bin/linux/ubuntu precise/" >> /etc/apt/sources.list
gpg --keyserver subkeys.pgp.net --recv E084DAB9
gpg --export --armor E084DAB9 | sudo apt-key add -
sudo apt-get update
sudo apt-get install r-base r-base-dev
sudo R CMD javareconf
