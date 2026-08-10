"""
Программа для отображение информации о ночной и дневной смене
"""
from shift12h.models.session import Session
from datetime import date, datetime, timedelta
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.style.pack import ROW
from toga.style.pack import CENTER
from shift12h.core.shift import ShiftCalculator
from shift12h.ui.date_input import DateInput
from shift12h.ui.date_picker import DatePicker
from shift12h.ui.style import MAIN_STYLE,DATE_TITLE_STYLE,DATE_INPUT_STYLE,SHIFT_BOX_STYLE,BUTTON_STYLE,SHIFT_VALUE_STYLE,SHIFT_TITLE_STYLE,NAV_STYLE





class Shift12H(toga.App):
    def startup(self):

        self.session = Session()

        self.shift = ShiftCalculator()

        self.txtDataSelection= DateInput(
             placeholder="dd.mm.yyyy",
             style = DATE_INPUT_STYLE,
            #  style=Pack(
            #      width=100,
            #      margin=(0, 8),
            #      ),
        )
        self.txtDataSelection.on_confirm=self.on_confirm

        self.date_picker = DatePicker(
            self,
            self.on_date_selected
         )

        self.date_button = toga.Button(
             "Выбрать дату",
             on_press=self.on_btn_select_date,
             style=BUTTON_STYLE,
            #  style=Pack(
            #      flex=1,
            #      margin=5
            #  )
        )
                                   
        self.btnToday=toga.Button(
            "Сегодня",
            on_press=self.btnToday_press,
            style = BUTTON_STYLE,
            # style=Pack(
            #     flex=1,
            #     margin=5
            # )
        )

        self.btnDo = toga.Button(
            "До", 
            #style=Pack(width=100, margin_right=10),
            style=Pack(margin_right=8, flex=1),
            #style=NAV_BUTTON_STYLE,  
            on_press=self.btnDo_press,
        )
        self.btnPosle = toga.Button(
            "После", 
            style=Pack(flex=1, margin_left=8),
            on_press=self.btnPosle_press,
        )

        # # Нижняя строка: кнопки навигации
        # nav_row = toga.Box(style=Pack(direction=ROW, align_items=CENTER, margin=(0,10,0,10)))
        # nav_row.add(self.btnDo)
        # nav_row.add(self.btnPosle)

        nav_row = toga.Box(
            children=[
                self.btnDo,
                self.btnPosle],
                style=NAV_STYLE,
            )
        

        # lbl1smena = toga.Label("1 смена: 19:00 - 7:00", style=Pack(margin_top=8),)      
        # lbl2smena = toga.Label("2 смена: 7:00 - 19:00", style=Pack(margin_top=8),)
        # self.lbl1smena_brigada = toga.Label("_", style=Pack(margin_top=8),)
        # self.lbl2smena_brigada = toga.Label("_", style=Pack(margin_top=8),)
        # spacer = toga.Box(style=Pack(flex=1))
        lbl1smena = toga.Label("1 смена: 19:00 - 7:00", style=SHIFT_TITLE_STYLE,)      
        lbl2smena = toga.Label("2 смена: 7:00 - 19:00", style=SHIFT_TITLE_STYLE,)
        self.lbl1smena_brigada = toga.Label("_", style=SHIFT_VALUE_STYLE,)
        self.lbl2smena_brigada = toga.Label("_", style=SHIFT_VALUE_STYLE,)
        
        
         # Верхняя строка: дата + кнопка
        date_row = toga.Box(style=Pack(direction=ROW, flex=1,align_items=CENTER, margin_bottom=10))
        date_row.add(toga.Label("Дата:", style=DATE_TITLE_STYLE)) #Pack(width=60, margin_right=8)
        date_row.add(self.txtDataSelection)

        date_buttons = toga.Box(
            children=[self.date_button, self.btnToday],
            style=BUTTON_STYLE,
            #style=Pack(direction=ROW, flex=1, margin_left=8)
        )    

        
        # Основной контейнер
        # content = toga.Box(
        #     style=Pack(
        #         direction=COLUMN,
        #         margin=20,
        #         align_items=CENTER,
        #         flex=1
        #     )
        # )
        content = toga.Box(style=MAIN_STYLE)

        self.lblSelectedDate = toga.Label("", style=Pack(margin_bottom=10))

        selected_date_box=toga.Box(
            children=[self.lblSelectedDate],
            style=Pack(
                direction=ROW, flex=1, align_items=CENTER, margin_bottom=10
            )
        )

        night_box = toga.Box(
            children=[
                lbl1smena, 
                self.lbl1smena_brigada, 
            ],
            style=Pack(
                direction=COLUMN,
                margin=16,
                flex=1
            )
        )

        day_box = toga.Box(
            children=[
                lbl2smena, 
                self.lbl2smena_brigada, 
            ],
            style=Pack(
                direction=COLUMN,
                margin=16,
                flex=1
            )
        )

        shift_box=toga.Box(
            children=[
                night_box, 
                day_box
            ],
            # style=Pack(
            #     direction=ROW,
            #     flex=1
            # )
            style=SHIFT_BOX_STYLE,
        )


        # Центральная "карточка"
        card = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=16,
                flex=1
            )
        )

        card.add(date_row)
        card.add(date_buttons)
        card.add(selected_date_box)
        card.add(shift_box)
        card.add(nav_row)

        content.add(card)

        self.main_window = toga.MainWindow(title="Программа для отображения информации о ночной и дневной смене")
        self.main_window.size = (350, 600)
        self.main_window.content = content
        self.main_window.show()

    def on_date_selected(self, selected_date):
        self.session.current_date = selected_date
        self.txtDataSelection.value = selected_date.strftime(
            "%d.%m.%Y"
        )
        self.update_shift()

    def on_btn_select_date(self, wdget):
        current_date = self.session.current_date

        if current_date is None:
            current_date = date.today() 

        self.date_picker.show(current_date)
            

    def btnDo_press(self,widget):
        date_selected = self.txtDataSelection.get_date()
        if date_selected is None:
            self.txtDataSelection.value = "Это не дата"
            return
        date_selected_new=date_selected-timedelta(days=1)
        self.on_date_selected(date_selected_new)

    def btnPosle_press(self, widget):
        date_selected = self.txtDataSelection.get_date()
        if date_selected is None:
            self.txtDataSelection.value = "Это не дата"
            return
        date_selected_new=date_selected+timedelta(days=1)
        self.on_date_selected(date_selected_new)



    def btnToday_press(self, widget):
        self.set_today()
        self.update_shift()

    def on_confirm(self, widget):
        #Получаем дату из текстового поля
        #Переводи её в объект date
        #Если она корректная то сохраняем в Seeeion.current_date и обновляем отображение смен
        date_selected = self.txtDataSelection.get_date()
        if date_selected is None:
            self.txtDataSelection.value = "Это не дата"
            return
        self.on_date_selected(date_selected)


    def set_today(self):
        #today=datetime.today()
#        self.txtDataSelection.value = today.strftime("%d.%m.%Y")
#        self.update_shift()
        today = date.today()
        self.on_date_selected(today)
        #self.update_shift()


    def update_shift(self):
        # current_date =  self.txtDataSelection.get_date() # Возвращает None Если такой даты нет
        # if current_date is None:
        #     self.lbl1smena_brigada.text = "Ошибка даты"
        #     self.lbl2smena_brigada.text = "Ошибка даты" 
        #     return    
        # night, day = self.shift.get_shift(current_date)
        # self.lbl1smena_brigada.text = f"Бригада №{night}"
        # self.lbl2smena_brigada.text = f"Бригада №{day}"
        #-------------------------------------------------

        current_date = self.txtDataSelection.get_date()


        # Возвращает None Если такой даты нет
        if current_date is None:
            return 
           
        self.session.current_date=current_date
        night, day = self.shift.get_shift(current_date)
        self.lblSelectedDate.text = f"Выбрана дата: {current_date.strftime('%d.%m.%Y')}"
        self.session.night_shift = night
        self.session.day_shift = day
        self.lbl1smena_brigada.text = f"Бригада №{night}"
        self.lbl2smena_brigada.text = f"Бригада №{day}"
        
        


        


def main():
    return Shift12H()
