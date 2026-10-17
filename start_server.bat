@echo off
title Stock Analyst Intelligence Dashboard Server
cd /d "%~dp0"
echo Starting Stock Analyst Intelligence Dashboard Server...
python serve_network.py
pause
