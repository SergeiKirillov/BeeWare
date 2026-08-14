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
        data_dir = Path(app.paths.data)


    except Exception as e:
        data_dir =  Path.home()/"shift12h"

    log_dir =  data_dir/"logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    return log_dir

def _is_android():
    """
    Проверка, что программа работает на Android.
    """

    return platform.system().lower() == "linux" and (
        "ANDROID_ARGUMENT" in os.environ
        or "ANDROID_PRIVATE" in os.environ
        or "ANDROID_ROOT" in os.environ
    )


def _get_internal_log_file():
    """
    Путь к внутреннему файлу логов приложения.
    """
    log_dir = get_log_directory()
    return log_dir / APP_LOG_NAME

class SafeFormatter(logging.Formatter):
    """
    Формат логов.
    Пример:
    2026-08-14 12:45:21 | INFO     | Приложение запущено
    """

    def format(self, record):
        return (
            f"{self.formatTime(record, '%Y-%m-%d %H:%M:%S')}"
            f" | {record.levelname:<8}"
            f" | {record.getMessage()}"
        )

def setup_logging(level=logging.INFO):
    """
    Настраивает систему логирования приложения.
    Возвращает logging.Logger.
    Использование:
        logger = setup_logging()
        logger.info("Приложение запущено")
        logger.error("Произошла ошибка")
    """

    logger = logging.getLogger("shift12h")

    # Не создаём обработчики повторно
    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = SafeFormatter()

    # ---------------------------------------------------------
    # 1. Запись во внутренний файл приложения
    # ---------------------------------------------------------

    log_file = _get_internal_log_file()

    try:
        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    except Exception:
        # Если запись в файл невозможна,
        # приложение всё равно должно продолжить работу.
        pass

    # ---------------------------------------------------------
    # 2. Вывод в консоль
    # ---------------------------------------------------------

    try:
        console_handler = logging.StreamHandler()

        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    except Exception:
        pass

    logger.info("========================================")
    logger.info("Система логирования запущена")
    logger.info("Платформа: %s", platform.system())
    logger.info("Файл лога: %s", log_file)
    logger.info("========================================")

    return logger

def get_log_file():
    """
    Возвращает путь к внутреннему файлу лога.
    """
    return _get_internal_log_file()


def export_log_to_android():
    """
    Копирует текущий лог в общедоступную папку Download
    на Android.

    Результат:
        Download/shift12h.log

    Возвращает:
        True  - если успешно
        False - если произошла ошибка
    """

    logger = logging.getLogger("shift12h")

    if not _is_android():
        logger.warning(
            "export_log_to_android(): программа работает не на Android"
        )
        return False

    source_file = _get_internal_log_file()

    if not source_file.exists():
        logger.warning("Файл лога отсутствует: %s", source_file)
        return False

    try:
        # -----------------------------------------------------
        # Android Java API через Chaquopy
        # -----------------------------------------------------

        from java import jclass

        PythonActivity = jclass(
            "org.beeware.android.MainActivity"
        )

        MediaStore = jclass(
            "android.provider.MediaStore"
        )

        ContentValues = jclass(
            "android.content.ContentValues"
        )

        Build = jclass(
            "android.os.Build"
        )

        activity = PythonActivity.singletonThis

        resolver = activity.getContentResolver()

        # -----------------------------------------------------
        # Для Android 10+ используем MediaStore.Downloads
        # -----------------------------------------------------

        if Build.VERSION.SDK_INT >= 29:

            values = ContentValues()

            values.put(
                MediaStore.MediaColumns.DISPLAY_NAME,
                APP_LOG_NAME,
            )

            values.put(
                MediaStore.MediaColumns.MIME_TYPE,
                "text/plain",
            )

            values.put(
                MediaStore.MediaColumns.RELATIVE_PATH,
                "Download/",
            )

            values.put(
                MediaStore.MediaColumns.IS_PENDING,
                1,
            )

            collection = MediaStore.Downloads.EXTERNAL_CONTENT_URI

            uri = resolver.insert(
                collection,
                values,
            )

            if uri is None:
                raise RuntimeError(
                    "MediaStore не вернул URI для файла"
                )

            try:

                # ---------------------------------------------
                # Записываем файл
                # ---------------------------------------------

                output_stream = resolver.openOutputStream(uri)

                if output_stream is None:
                    raise RuntimeError(
                        "Не удалось открыть OutputStream"
                    )

                try:

                    with open(source_file, "rb") as source:

                        while True:

                            data = source.read(8192)

                            if not data:
                                break

                            output_stream.write(data)

                    output_stream.flush()

                finally:

                    output_stream.close()

                # ---------------------------------------------
                # Публикуем файл
                # ---------------------------------------------

                values = ContentValues()

                values.put(
                    MediaStore.MediaColumns.IS_PENDING,
                    0,
                )

                resolver.update(
                    uri,
                    values,
                    None,
                    None,
                )

            except Exception:

                # Если запись не завершилась,
                # удаляем незавершённый объект.
                try:
                    resolver.delete(
                        uri,
                        None,
                        None,
                    )
                except Exception:
                    pass

                raise

        else:

            # -------------------------------------------------
            # Старые Android
            # -------------------------------------------------

            from java import jclass

            Environment = jclass(
                "android.os.Environment"
            )

            download_dir = Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DOWNLOADS
            )

            download_dir.mkdirs()

            destination = os.path.join(
                str(download_dir),
                APP_LOG_NAME,
            )

            with open(source_file, "rb") as source:
                with open(destination, "wb") as destination_file:

                    while True:

                        data = source.read(8192)

                        if not data:
                            break

                        destination_file.write(data)

        logger.info(
            "Лог экспортирован в Download/%s",
            APP_LOG_NAME,
        )

        return True

    except Exception:

        logger.exception(
            "Не удалось экспортировать лог в Download"
        )

        return False
