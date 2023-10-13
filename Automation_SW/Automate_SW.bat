@echo off

SETLOCAL

set mypath="%~dp0"

cd main

start "Starting Program" main.exe

ENDLOCAL

