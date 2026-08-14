import logging
import os
import platform
import shutil
from pathlib import Path
from logging.handlers import RotatingFileHandler


APP_LOG_NAME = "shift12h.log"


def get_log_directory():
    """Возвращает папку для внутренних логов приложения."""

    try:
        import toga

        app = toga.App.app
        data_dir = Path(app.paths.data)

    except Exception:
        data_dir = Path.home() / ".shift12h"

    log_dir = data_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    return log_dir


def get_log_file():
    """Возвращает полный путь к текущему файлу лога."""

    return get_log_directory() / APP_LOG_NAME


class LogFormatter(logging.Formatter):
    """Формат строк журнала."""

    def format(self, record):
        return (
            f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')}"
            f" | {record.levelname:<8}"
            f" | {record.getMessage()}"
        )


def setup_logging(level=logging.INFO):
    """
    Инициализирует систему логирования.

    Возвращает:
        logging.Logger
    """

    logger = logging.getLogger("shift12h")

    # Не создаём обработчики повторно
    if logger.handlers:
        return logger

    logger.setLevel(level)

    log_file = get_log_file()

    formatter = LogFormatter()

    # --------------------------------------------------
    # Файл лога
    # --------------------------------------------------

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,   # 1 МБ
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # --------------------------------------------------
    # Консоль
    # --------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.info("----------------------------------------")
    logger.info("Запуск системы логирования")
    logger.info("Платформа: %s", platform.system())
    logger.info("Файл: %s", log_file)
    logger.info("----------------------------------------")

    return logger


def save_log_to_download():
    """
    Копирует текущий лог в общедоступную папку Download.

    Возвращает:
        Path — путь к сохранённому файлу
        None — если произошла ошибка
    """

    logger = logging.getLogger("shift12h")

    source = get_log_file()

    if not source.exists():
        logger.error(
            "Файл лога не найден: %s",
            source,
        )
        return None

    try:

        # ----------------------------------------------
        # Android
        # ----------------------------------------------

        if (
            platform.system().lower() == "linux"
            and (
                "ANDROID_ARGUMENT" in os.environ
                or "ANDROID_PRIVATE" in os.environ
                or "ANDROID_ROOT" in os.environ
            )
        ):

            from java import jclass

            Environment = jclass(
                "android.os.Environment"
            )

            download_dir = (
                Environment.getExternalStoragePublicDirectory(
                    Environment.DIRECTORY_DOWNLOADS
                )
            )

            download_dir.mkdirs()

            destination = Path(
                str(download_dir)
            ) / APP_LOG_NAME

        # ----------------------------------------------
        # Linux / Windows
        # ----------------------------------------------

        else:

            destination = (
                Path.home()
                / "Downloads"
                / APP_LOG_NAME
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        # ----------------------------------------------
        # Копирование
        # ----------------------------------------------

        shutil.copy2(
            source,
            destination,
        )

        logger.info(
            "Лог сохранён: %s",
            destination,
        )

        return destination

    except Exception:

        logger.exception(
            "Ошибка сохранения лога в Download"
        )

        return None