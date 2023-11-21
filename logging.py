import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOG_BASE_PATH, exist_ok=True)

# Получение объекта логгера для приложения app1
logger = logging.getLogger('main_api')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = TimedRotatingFileHandler(
    os.path.join(LOG_BASE_PATH, 'main_api.log'),
    when='W0',  # Запуск ротации каждую неделю (W0 - начало недели)
    interval=1,  # Интервал в неделях
    backupCount=5  # Хранить последние 5 архивных файлов
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)