#!/bin/bash

if [ $# -eq 0 ] 
then
	echo './jenkins.sh [PORT]'
	exit 1
else
	java -jar jenkins.war --httpPort=$1
fi

