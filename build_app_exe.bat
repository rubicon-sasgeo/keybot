cd ./src
pyinstaller --onefile main.py
cd dist
del keybot.exe
ren main.exe keybot.exe
cd ..
cd ..
