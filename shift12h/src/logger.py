import logging  
import os
import platform
from pathlib import Path

APP_LOG_NAME = "shift12h.log"

def get_log_directory():
    """
    Возвращает внутреннюю папку приложения для временного/рабочего лога.
    На Android:
        <внутреннее хранилище приложения>/logs
    На Linux/Windows:
        папка logs рядом с пользовательскими данными приложения.
    """
    try:
        import toga

        app=toga.App.app

        # Toga/Briefcase application paths
        data_
    except Exception as e:
        raise e