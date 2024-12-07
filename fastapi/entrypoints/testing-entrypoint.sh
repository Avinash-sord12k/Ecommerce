#!/bin/bash

echo "> ============================="
echo "> Environment Settings"
echo "> ============================="
env
echo "> ============================="
echo "..."

echo "> ============================="
echo "> Activating Python Environment"
echo "> ============================="
source venv/bin/activate
echo "> Done"
echo "..."

echo "> ============================="
echo "> Change owner for shared folder"
echo "> ============================="
sudo chown appuser:appuser /home/appuser/shared
echo "> Done"
echo "..."

echo "> ============================="
echo "> Running Pytest               "
echo "> ============================="
exec pytest app/ -v -s
