@echo off
rem exeを作成
pyinstaller ..\python\sifacns_ranking.py --onefile --clean

rem exeをexeフォルダに移動
del ..\exe\sifacns_ranking.exe
move .\dist\sifacns_ranking.exe ..\exe\sifacns_ranking.exe

rem 不要なファイルを削除
rd /s /q .\build
rd /s /q ..\python\__pycache__
del .\sifacns_ranking.spec
rd /s /q .\dist

pause