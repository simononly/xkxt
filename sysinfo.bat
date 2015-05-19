@echo off
echo ======SYSTEM INFORMATION======>sysinfo.txt
echo whoami:>>sysinfo.txt
whoami>>sysinfo.txt
echo ==============================>>sysinfo.txt
echo ipconfig:>>sysinfo.txt
ipconfig>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo net user:>>sysinfo.txt
net user>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo net start:>>sysinfo.txt
net start>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo tasklist:>>sysinfo.txt
tasklist /v>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo localgroup:>>sysinfo.txt
net localgroup administrators>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo netstat:>>sysinfo.txt
netstat -ano >>sysinfo.txt
echo ===============================>>sysinfo.txt
echo net view:>>sysinfo.txt
net view>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo net view /domain:>>sysinfo.txt
net view /domain>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo c:>>sysinfo.txt
dir c:\>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo d:>>sysinfo.txt
dir d:\>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo e:>>sysinfo.txt
dir e:\>>sysinfo.txt
echo ===============================>>sysinfo.txt
echo desktop:>>sysinfo.txt
dir "c:\Documents and Settings\Administrator\×ÀÃæ">>sysinfo.txt
echo ===============================>>sysinfo.txt
exit

