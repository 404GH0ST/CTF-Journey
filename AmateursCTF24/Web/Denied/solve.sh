#!/usr/bin/env bash

curl -I -s http://denied.amt.rs/ | grep -oP "(?<=flag=).+(?=;)" | php -R 'echo urldecode($argn)."\n";'
