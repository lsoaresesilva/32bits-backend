#!/bin/bash

git pull origin master
sudo /etc/init.d/nginx stop
sudo /etc/init.d/nginx start