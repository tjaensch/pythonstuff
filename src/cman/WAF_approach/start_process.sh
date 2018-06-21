#!/bin/bash

echo 'digging up files from https://data.nodc.noaa.gov/ndbc/cmanwx/ which can take up to an hour...'
lftp https://data.nodc.noaa.gov/ndbc/cmanwx/ -e "du -a | awk '/nc/' | awk '/NDBC/' | cut -d '/' -f2- >> files.txt;quit"

python cman_nc2iso.py