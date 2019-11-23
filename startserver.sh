#!/bin/sh

cd /home/pi/www
mpg123 --fifo /home/pi/www/fifo/mpg123 -R asdf > /home/pi/www/log/log.txt &
/home/pi/www/outputparser.pl &
