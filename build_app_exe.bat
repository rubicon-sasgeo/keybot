REM build exe
cd ./src
pyinstaller --onefile main.py
cd dist
REM rename exe
del keybot.exe
ren main.exe keybot.exe
REM copy config file from root
copy ..\..\config.toml
REM copy bots
md bots
cd bots
del *.json
copy ..\..\..\bots\*.json .
REM move back to root dir.
cd ..
cd ..
cd ..
