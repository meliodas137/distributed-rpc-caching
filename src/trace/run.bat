start "msc" cmd /k msc.bat
start "msb" cmd /k msb.bat
start "lb" cmd /k lb.bat
TIMEOUT /T 2
for /l %%x in (1, 1, 100) do npm run msa
