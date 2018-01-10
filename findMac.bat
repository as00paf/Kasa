@echo off
set mac=%1
for /L %%a in (1,1,254) do @start /b ping 192.168.1.%%a -w 100 -n 2 >nul
arp -a | find /i %mac%