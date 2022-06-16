#!/bin/sh

cd src
pyinstaller --onefile qt_window.py --distpath ./../ --name XianXia
