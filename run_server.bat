@echo off
echo Activando el entorno virtual e iniciando el servidor de Django...
call .venv\Scripts\activate.bat
python manage.py runserver
