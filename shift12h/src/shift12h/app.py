"""
Программа для отображение информации о ночной и дневной смене
"""
from shift12h.models.session import Session
from shift12h.core.wotkerdb import WorkerDB
from shift12h.worker_card import WorkerCard
from shift12h.worker_card import BrigadeWindows
from datetime import date, datetime, timedelta
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.style.pack import ROW
from toga.style.pack import CENTER
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

        self.main_window = toga.MainWindow(title="Программа для отображения информации о ночной и дневной смене")
        self.main_window.size = (360, 740)
        self.main_window.content = content
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

        
        worker_db = WorkerDB()
        workers = worker_db.get_workers_by_brigade(brigade_number)

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

        


        


def main():
    return Shift12H()



#[ ]: Изменение интерфейса для адаптивности
#[ ]: Календарь на Android
#[ ]: Информация о пользователях бригады с телефонами и возможность вызова из программы 
#[ ]: Изменить значки программы и меню в программе