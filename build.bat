@echo off
echo Gerando executavel do RPG Ficha...
echo.

REM Limpa builds anteriores
rmdir /s /q build
rmdir /s /q dist
del /q ficha_rpg.spec

REM Executa PyInstaller
python -m PyInstaller --onefile --noconsole --add-data "icons;icons" ficha_rpg.py

echo.
echo Executavel gerado em dist\rpg_ficha.exe
pause