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


from shift12h.models.session import Session
from shift12h.core.wotkerdb import WorkerDB
from shift12h.worker_card import WorkerCard
from shift12h.worker_card import BrigadeWindows

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
            on_press=self.open_brigade
            )
        self.btn2smena_brigada = toga.Button(
            "_", 
            style=BUTTON_STYLE,
            on_press=self.open_brigade,
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
        content = toga.Box(
            children=[
                box_data_select,
                box_content,
                nav_row
            ],
            style=MAIN_STYLE)
    #---------------------------------------
        #добавление пункта меню
        settion_group = toga.Group(
            "Настройки",
            order=0,
        )
        select_file_command = toga.Command(
            self.select_personal_file,
            text="Выбрать файл картотеки",
            group=settion_group,
        )

    #---------------------------------------

        self.main_window = toga.MainWindow(title="Программа для отображения информации о ночной и дневной смене")
        self.main_window.size = (360, 740)
        self.main_window.content = content
        self.commands.add(select_file_command)
        self.main_window.show()

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
        brigade_number = widget.text.replace("Бригада №", "")

        
        #worker_db = WorkerDB()
        personal_file = Path(self.paths.data) / "personal.json"
        worker_db = WorkerDB(personal_file)
        workers = worker_db.get_workers_by_brigade(brigade_number)

        if workers is not None:
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
        target = Path(self.paths.data) / "personal.json"

        if target.exists():
            return

        source = Path(__file__).parent / "data" / "personal.json"

        if source.exists():
            shutil.copy2(source, target)
       


        


def main():
    return Shift12H()



#[ ]: Изменение интерфейса для адаптивности
#[ ]: Календарь на Android
#[ ]: Информация о пользователях бригады с телефонами и возможность вызова из программы 
#[ ]: Изменить значки программы и меню в программе