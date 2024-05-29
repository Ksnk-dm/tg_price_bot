import sys
import os

# Добавляем путь к директории с вашим приложением
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем ваш основной файл
import main as app

# Функция для старта приложения
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Bot is running!"]