#!/bin/bash

sudo killall gpsd
sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock