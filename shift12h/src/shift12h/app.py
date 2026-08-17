"""
Программа для отображение информации о ночной и дневной смене
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.style.pack import ROW
from toga.style.pack import CENTER

from datetime import date, datetime, timedelta
from pathlib import Path
import shutil
import json
import os


from shift12h.models.session import Session
from shift12h.core.wotkerdb import WorkerDB
from shift12h.worker_card import WorkerCard
from shift12h.worker_card import BrigadeWindows
from shift12h.worker_card import BrigadeWindows2

#from shift12h.logger_1 import setup_logging
#from shift12h.logger_1 import get_log_file, export_log_to_android

from shift12h.logger import setup_logging, save_log_to_download, get_log_file

from shift12h.core.shift import ShiftCalculator
from shift12h.ui.date_input import DateInput
from shift12h.ui.date_picker import DatePicker
from shift12h.ui.style import (
    MAIN_STYLE,
    BOX_DATA_SELECT,
    BOX_DATA_SELECT_TITLE,
    BOX_DATA_SELECT_BUTTON,
    BOX_CONTENT,
    BOX_CONTENT_DATA,
    BOX_CONTENT_INFO,
    BOX_CONTENT_INFO_NIGHT,
    BOX_CONTENT_INFO_DAY,
    BOX_SELECT_DAY_BUTTON,


    DATE_TITLE_STYLE,
    DATE_INPUT_STYLE,
    BUTTON_STYLE,
    SHIFT_VALUE_STYLE,
    SHIFT_TITLE_STYLE,
)



class Shift12H(toga.App):
    def startup(self):
        self.logger = setup_logging()
        self.logger.info("Выбрана дата: %s", datetime.today())
        self.logger.info("Приложение Shift12H запущено")

        self.install_default_personal()

        self.session = Session()
        self.shift = ShiftCalculator()

        self.create_interface()
        self.update_shift(
            self.session.current_date
        )
        

    
    def create_interface(self): 
#---------------------------------------------------------------------------------------------

    #------Часть для выбора дня
        lblDataTitle = toga.Label(
            "Дата:", 
            style=DATE_TITLE_STYLE
        )

        self.txtDataSelection= DateInput(
             placeholder="dd.mm.yyyy",
             style = DATE_INPUT_STYLE,   
        )
        self.txtDataSelection.on_confirm=self.on_confirm

        self.date_picker = DatePicker(
            self,
            self.on_date_selected
        )

         # Верхняя строка: дата + кнопка
        date_row = toga.Box(
            children=[
                lblDataTitle,
                self.txtDataSelection,
            ],
            style = BOX_DATA_SELECT_TITLE,
        )
        

        self.date_button = toga.Button(
             "Выбрать дату",
             on_press=self.on_btn_select_date,
             style=BUTTON_STYLE,
        )                  

        # self.date_button = toga.Button(
        #       "Выбрать картотеку",
        #       on_press=self.select_personal_file,
        #       style=BUTTON_STYLE,
        #  ) 

        self.btnToday=toga.Button(
            "Сегодня",
            on_press=self.btnToday_press,
            style = BUTTON_STYLE, 
        )
        date_buttons = toga.Box(
            children=[
                self.date_button, 
                self.btnToday
            ],
            style = BOX_DATA_SELECT_BUTTON,
        )   

        box_data_select = toga.Box(
            children=[
                date_row,
                date_buttons,
            ],
            style=BOX_DATA_SELECT,
        ) 
    
    #------Часть отвечающая вывода информации о бригадах

        self.lblSelectedDate = toga.Label("", style=DATE_TITLE_STYLE)
        lbl1smena = toga.Label(
            "1 смена: 19:00 - 7:00", 
            style=SHIFT_TITLE_STYLE,
        )      
        lbl2smena = toga.Label(
            "2 смена: 7:00 - 19:00", 
            style=SHIFT_TITLE_STYLE,
        )
        self.btn1smena_brigada = toga.Button(
            "_", 
            style=BUTTON_STYLE,
            #on_press=self.open_brigade
            on_press=self.open_window
            #on_press=self.open_dialog
            )
        self.btn2smena_brigada = toga.Button(
            "_", 
            style=BUTTON_STYLE,
            # on_press=self.open_brigade,  # Работает на linux, но не работает на Android
            on_press=self.open_window  #Работает на linux, работает на Android
            )

        box_content_data=toga.Box(
            children=[self.lblSelectedDate],
            style=BOX_CONTENT_DATA,
        )

        box_content_info_night = toga.Box(
            children=[
                lbl1smena, 
                self.btn1smena_brigada, 
            ],
            style=BOX_CONTENT_INFO_NIGHT
        )

        box_content_info_day = toga.Box(
            children=[
                lbl2smena, 
                self.btn2smena_brigada, 
            ],
            style=BOX_CONTENT_INFO_DAY
        )

        box_content_info = toga.Box(
            children=[
                box_content_info_night,
                box_content_info_day,
            ],
            style=BOX_CONTENT_INFO
        )

        box_content=toga.Box(
            children=[
                box_content_data,
                box_content_info
            ],
            style=BOX_CONTENT,
        )


    #------Кнопки предыдущий - следующий деень
        self.btnDo = toga.Button(
            "До", 
            style=BUTTON_STYLE,
            on_press=self.btnDo_press,
        )
        self.btnPosle = toga.Button(
            "После", 
            style = BUTTON_STYLE,
            on_press=self.btnPosle_press,
        )
        nav_row = toga.Box(
            children=[
                self.btnDo,
                self.btnPosle],
                style=BOX_SELECT_DAY_BUTTON
            )
    #-------------------------------------


        # Основной контейнер
        self.content = toga.Box(
            children=[
                box_data_select,
                box_content,
                nav_row
            ],
            style=MAIN_STYLE)
    #---------------------------------------
        # #добавление пункта меню
        # settion_group = toga.Group(
        #     "Настройки",
        #     order=0,
        # )
        # select_file_command = toga.Command(
        #     self.select_personal_file,
        #     text="Выбрать файл картотеки",
        #     group=settion_group,
        # )
    #---------------------------------------
        #добавление пункта меню
        settion_group = toga.Group(
            "Настройки",
            order=0,
        )
        # select_file_command = toga.Command(
        #     self.save_log_0,
        #     text="Сохранить лог НА ТЕЛЕФОНЕ",
        #     group=settion_group,
        # )
        # select_file_command_test = toga.Command(
        #     self.test_copy_log,
        #     text="Тест записи на телефон",
        #     group=settion_group,
        # )
            
        select_file_command_save = toga.Command(
             self.save_log,
             text="Сохранение лога",
             group=settion_group
         )


    #---------------------------------------

        self.main_window = toga.MainWindow(title="Программа для отображения информации о ночной и дневной смене")
        self.main_window.size = (360, 740)
        self.main_window.content = self.content
        self.commands.add(select_file_command_save)
        self.main_window.show()

    def save_log_0(self, widget):
        result = save_log_to_download()

        if result is not None:
            self.logger.info(
                "Журнал сохранён пользователем"
            )
        else:
            self.logger.error(
                "Не удалось сохранить журнал"
            )

    def save_log(self, widget):
        import os
        import shutil

        try:
            source = get_log_file()

            print("SOURCE:", source)
            print("EXISTS:", source.exists())

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

            destination = os.path.join(
                str(download_dir),
                "shift12h.log"
            )

            print("DESTINATION:", destination)

            shutil.copy2(
                source,
                destination
            )

            print("COPY OK")

        except Exception as e:
            print("COPY ERROR:", repr(e))

    def on_date_selected(self, selected_date):
        self.session.current_date = selected_date
        self.txtDataSelection.value = selected_date.strftime(
            "%d.%m.%Y"
        )
        self.update_shift(selected_date)

    def on_btn_select_date(self, wdget):
        current_date = self.session.current_date

        if current_date is None:
            current_date = date.today() 

        self.date_picker.show(current_date)
            

    def btnDo_press(self,widget):
        # date_selected = self.txtDataSelection.get_date()
        # if date_selected is None:
        #     self.txtDataSelection.value = "Это не дата"
        #     return

        date_selected_new=self.session.current_date-timedelta(days=1)
        self.update_shift(date_selected_new)

        #self.on_date_selected(date_selected_new)

    def btnPosle_press(self, widget):
        # date_selected = self.txtDataSelection.get_date()
        # if date_selected is None:
        #     self.txtDataSelection.value = "Это не дата"
        #     return
        date_selected_new=self.session.current_date+timedelta(days=1)
        self.update_shift(date_selected_new)



    def btnToday_press(self, widget):
        self.set_today()
        #self.update_shift()

    def on_confirm(self, widget):
        #Получаем дату из текстового поля
        #Переводи её в объект date
        #Если она корректная то сохраняем в Seeeion.current_date и обновляем отображение смен
        date_selected = self.txtDataSelection.get_date()
        if date_selected is None:
            self.txtDataSelection.value = "Это не дата"
            return
        #self.on_date_selected(date_selected)
        self.update_shift(date_selected)


    def set_today(self):
        today = date.today()
        #self.on_date_selected(today)
        self.update_shift(today)


    def update_shift(self, selected_date:date):
        
        #current_date = self.txtDataSelection.get_date()

        self.txtDataSelection.value = selected_date.strftime("%d.%m.%Y")   

        # Возвращает None Если такой даты нет
        if selected_date is None:
            return 
           
        self.session.current_date=selected_date
        night, day = self.shift.get_shift(selected_date)
        self.lblSelectedDate.text = f"Выбрана дата: {selected_date.strftime('%d.%m.%Y')}"
        self.session.night_shift = night
        self.session.day_shift = day
        self.btn1smena_brigada.text = f"Бригада №{night}"
        self.btn2smena_brigada.text = f"Бригада №{day}"

    def open_brigade(self, widget):
        self.logger.info(f"-----Заходим в функцию нажатия на бригаду------")
        brigade_number = widget.text.replace("Бригада №", "")

        
        #worker_db = WorkerDB()
        personal_file = Path(self.paths.data) / "personal.json"
        self.logger.info(f"Событие при нажатии на кнопку бригады / путь к файлу({personal_file})")
        worker_db = WorkerDB(personal_file)
        workers = worker_db.get_workers_by_brigade(brigade_number)

        if workers is not None:
            #self.logger.info(f"Кол-во найденных пользователей {workers}")
            
            window = BrigadeWindows(
                                self,
                                brigade_number,
                             workers,
                            )
            window.show()
            

        # #self.show_workers(brigade_number)
        

        # windowsTwo = toga.Window(
        #     title=f"Информация о бригаде №{brigade_number}"
        # )

        # lblTitle = toga.Label(
        #     f"Сейчас работает бригада №{brigade_number}",
        #     style=Pack(
        #         margin=20,
        #     )
        # )

        # self.worker_box = toga.Box(
        #     style=Pack(
        #         direction=COLUMN,
        #         flex=1,
        #     )
        # )
        
        # windowsTwo.content = lblTitle
        # windowsTwo.show()

    def show_workers(self, brigade):
        #self.workers_box.clear()
        workers = self.worker_db.get_workers_by_brigade(brigade)
        # for worker in workers:
        #     card = WorkerCard(worker)
        #     self.workers_box.add(card)
        window = BrigadeWindows(
            self,
            brigade,
            workers,
        )
        window.show()

    async def select_personal_file(self, widget):

        #print(toga.__version__)
        #print(hasattr(toga, "OpenFileDialog"))
        #print(hasattr(toga, "FileDialog"))

        try:
             # ---------------------------------------------------------
             # 1. Открываем диалог выбора файла
             # ---------------------------------------------------------
            result = await self.main_window.dialog(
                toga.OpenFileDialog(
                    title="Выберите файл картотеки",
                )
            )
            # Пользователь нажал "Отмена"
            if not result:
                return   

            result = Path(result)

            # ---------------------------------------------------------
            # 2. Проверяем расширение
            # ---------------------------------------------------------
            if result.suffix.lower() != ".json":
                await self.main_window.dialog(
                    toga.ErrorDialog(
                        "Ошибка",
                        "Выберите файл картотеки в формате JSON.",
                    )
                )
                return
            #-----------------------------------------------------------
            #  Проверяем стуктуру
            #-----------------------------------------------------------

            is_valid, message = self.validate_personal_json(
                    result
            )
            if not is_valid:
                await self.main_window.dialog(
                    toga.ErrorDialog(
                        "Ошибка картотеки",
                        message,
                    )
                )
                return


            # ---------------------------------------------------------
            # 3. Определяем место хранения картотеки
            # ---------------------------------------------------------
            data_folder = Path(self.paths.data)

            # На всякий случай создаём папку
            data_folder.mkdir(parents=True, exist_ok=True)

            target_file = data_folder / "personal.json"

            # ---------------------------------------------------------
            # 4. Копируем выбранный файл
            # ---------------------------------------------------------
            shutil.copy2(result, target_file)

            # ---------------------------------------------------------
            # 5. Сообщаем пользователю об успехе
            # ---------------------------------------------------------
            await self.main_window.dialog(
                toga.InfoDialog(
                    "Картотека",
                    f"Файл успешно сохранён:\n\n{target_file}",
                )
            )

            print(f"Исходный файл: {result}")
            print(f"Рабочая картотека: {target_file}")
            
        except Exception as e:
        # ---------------------------------------------------------
        # Обработка ошибок
        # ---------------------------------------------------------
            print(f"Ошибка при выборе картотеки: {e}")

            await self.main_window.dialog(
                toga.ErrorDialog(
                    "Ошибка",
                    f"Не удалось сохранить файл картотеки:\n\n{e}",
                )
            )


    def validate_personal_json(self, file_path):
        try:
             with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            return False, f"Некорректный JSON:\n{e}"
        except OSError as e:
            return False, f"Не удалось прочитать файл:\n{e}"


        # ---------------------------------------------------------
        # Корень JSON
        # ---------------------------------------------------------
        if not isinstance(data, dict):
            return False, "Корень JSON должен быть объектом."

        # ---------------------------------------------------------
        # workers
        # ---------------------------------------------------------
        if "workers" not in data:
            return False, "Отсутствует поле 'workers'."

        workers= data["workers"]

        if not isinstance(workers, list):
            return False, "Поле 'workers' должно быть списком."

        if not workers:
            return False, "Список 'workers' пуст."

        # ---------------------------------------------------------
        # Проверяем работников
        # ---------------------------------------------------------
        required_fields = {
            "id": int,
            "brigade": int,
            "fio": str,
            "shop": str,
            "position": str,
            "phone": str,
        }

        for index, worker in enumerate(workers, start=1):

            if not isinstance(worker, dict):
                return False, (
                    f"Работник №{index} должен быть объектом."
            )

            # Проверяем наличие и тип каждого поля
            for field, expected_type in required_fields.items():

                if field not in worker:
                    return False, (
                        f"Работник №{index}: "
                        f"отсутствует поле '{field}'."
                    )

                if not isinstance(worker[field], expected_type):
                    return False, (
                        f"Работник №{index}: "
                        f"поле '{field}' должно иметь тип "
                        f"{expected_type.__name__}."
                )

            # -----------------------------------------------------
            # Проверяем номер бригады
            # -----------------------------------------------------
            if worker["brigade"] not in (1, 2, 3, 4):
                return False, (
                    f"Работник №{index}: "
                    f"недопустимый номер бригады "
                    f"{worker['brigade']}."
                )

            # -----------------------------------------------------
            # Проверяем обязательные строки
            # -----------------------------------------------------
            for field in ("fio", "shop", "position"):
                if not worker[field].strip():
                    return False, (
                        f"Работник №{index}: "
                        f"поле '{field}' не должно быть пустым."
                )

        return True, "Файл картотеки корректен."

    def install_default_personal(self):
        self.logger.info("Выбрана дата: %s", datetime.today())
        target = Path(self.paths.data) / "personal.json"
        self.logger.info(f" Папка для хранения пользовательских данных = {target}")
        #локальная папка для хранения данных приложения
        if target.exists():
            self.logger.info(f"Файл по этому пути существует и мы выходим ")
            # Файл существует
            return
        else:
            self.logger.info(f"Файл по этому пути НЕ существует")

        source = Path(__file__).parent / "data" / "personal.json"
        self.logger.info(f" Источник данных = {source}")
        # путь где должен лежать исходный файл
        if source.exists():
            #Источник существует 
            self.logger.info(f"Источник по этому пути существует. КОПИРУЕМ")
            shutil.copy2(source, target)
            if target.exists():
                self.logger.info(f"Файл по пути {target} существует и продолжаем ")
            else:
                self.logger.info(f"Файл по пути {target} НЕ существует")


       
    def test_download(self, widget):
        try:
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

            file_path = os.path.join(
                str(download_dir),
                "test_download.txt"
            )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(
                    "Тест записи в Download\n"
                    "Файл успешно создан приложением.\n"
                )

            print("Файл создан:", file_path)

        except Exception as e:
            print("ОШИБКА:", e)

    def test_copy_log_2(self, widget):
        try:
            import os
            import shutil

            source = get_log_file()

            print("Источник:")
            print(source)

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

            destination = os.path.join(
                str(download_dir),
                "shift12h.log"
            )

            shutil.copy2(
                source,
                destination
            )

            print("Лог успешно скопирован:")
            print(destination)

        except Exception as e:
            print("ОШИБКА:")
            print(e)

    def test_copy_log(self, widget):
        try:
            import os
            import shutil

            source = get_log_file()

            print("Источник:")
            print(source)

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

            destination = os.path.join(
                str(download_dir),
                "shift12h.log"
            )

            shutil.copy2(
                source,
                destination
            )

            print("Лог успешно скопирован:")
            print(destination)

        except Exception as e:
            print("ОШИБКА:")
            print(e)
    # Пример создания второго окна по нажатию
    def open_window(self, widget):
        
        new_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        brigade_number = widget.text.replace("Бригада №", "")
        new_box.add(toga.Label(f"Бригада №{brigade_number}", style=Pack(padding=5)))
        self.logger.info(f"-----Заходим в функцию отображения информации о бригаде №{brigade_number}------")
        #worker_db = WorkerDB()
        personal_file = Path(self.paths.data) / "personal.json"
        self.logger.info(f"Событие инфо бригады -> путь к файлу({personal_file})")
        worker_db = WorkerDB(personal_file)
        workers = worker_db.get_workers_by_brigade(brigade_number)

        if workers is not None:
            #self.logger.info(f"Кол-во найденных пользователей {workers}")
            contentBr = BrigadeWindows2(self, brigade_number, workers,)
            new_box = contentBr.content
            new_box.add(toga.Button("Вернуться назад", on_press=lambda widget: setattr(widget.window, 'content', self.content),))
            #-----------------------------------------------------------------------------    
            self.main_window.content = new_box
            self.main_window.show() # Показываем окно   

    async def open_dialog(self, widget):
        await self.main_window.info_dialog("Заголовок", "Сообщение при нажатии")

    async def message_dialog(self, widget, title, message):
        await self.main_window.info_dialog(title, message)


def main():
    return Shift12H()



#[ ]: Изменение интерфейса для адаптивности
#[ ]: Календарь на Android
#[ ]: Информация о пользователях бригады с телефонами и возможность вызова из программы 
#[ ]: Изменить значки программы и меню в программе