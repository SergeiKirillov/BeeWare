"""
Программа для отображение информации о ночной и дневной смене
"""
from shift12h.models.session import Session
from datetime import datetime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.style.pack import ROW
from toga.style.pack import CENTER
from shift12h.core.shift import ShiftCalculator



class Shift12H(toga.App):
    def startup(self):

        self.session = Session()

        self.shift = ShiftCalculator()

        self.txtDataSelection= toga.TextInput(
            placeholder="dd.mm.yyyy",
            style=Pack(
                width=100,
                padding=(0, 8),
                ),
        )
        self.txtDataSelection.on_confirm=self.on_confirm
                                   
        self.btnToday=toga.Button(
            "Сегодня",
            on_press=self.btnToday_press,
            style=Pack(
                flex=1,
            )
        )

        self.btnDo = toga.Button(
            "До", 
            #style=Pack(width=100, margin_right=10),
            style=Pack(margin_right=8, flex=1),
            on_press=self.btnDo_press,
        )
        self.btnPosle = toga.Button(
            "После", 
            style=Pack(flex=1, margin_left=8),
            on_press=self.btnPosle_press,
        )

        lbl1smena = toga.Label("1 смена: 19:00 - 7:00", style=Pack(padding_top=8),)      
        lbl2smena = toga.Label("2 смена: 7:00 - 19:00", style=Pack(padding_top=8),)
        self.lbl1smena_brigada = toga.Label("_", style=Pack(padding_top=8),)
        self.lbl2smena_brigada = toga.Label("_", style=Pack(padding_top=8),)
        spacer = toga.Box(style=Pack(flex=1))
        
         # Верхняя строка: дата + кнопка
        date_row = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding_bottom=10))
        date_row.add(toga.Label("Дата:", style=Pack(width=60, padding_right=8)))
        date_row.add(self.txtDataSelection)
        date_row.add(self.btnToday)

        # Нижняя строка: кнопки навигации
        nav_row = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=(0,10,0,10)))
        nav_row.add(self.btnDo)
        nav_row.add(self.btnPosle)

         # Основной контейнер
        content = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=20,
                alignment=CENTER,
                flex=1
            )
        )

        # Центральная "карточка"
        card = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=16,
                flex=1
            )
        )

        card.add(date_row)
        card.add(lbl1smena)
        card.add(self.lbl1smena_brigada)
        card.add(lbl2smena)
        card.add(self.lbl2smena_brigada)
        card.add(spacer)

        card.add(nav_row)

        content.add(card)

        self.main_window = toga.MainWindow(title="Программа для отображения информации о ночной и дневной смене")
        self.main_window.size = (350, 300)
        self.main_window.content = content
        self.main_window.show()

    def btnDo_press(self,widget):
        pass

    def btnPosle_press(self, widget):
        pass

    def btnToday_press(self, widget):
        self.set_today()
        self.update_shift()

    def on_confirm(self, widget):
        self.update_shift()    
      

    def set_today(self):
        today=datetime.today()
        self.session.current_date = today
        self.txtDataSelection.value = today.strftime("%d.%m.%Y")

        #night, day = self.shift.get_shift(today)
        #self.lbl1smena_brigada.text = f"Бригада №{night}"
        #self.lbl2smena_brigada.text = f"Бригада №{day}"
        
        



    def update_shift(self):
        try:
            current_date =datetime.strptime(self.txtDataSelection.value, "%d.%m.%Y").date()
        except ValueError:
            self.lbl1smena_brigada.text = "Ошибка даты"
            self.lbl2smena_brigada.text = "Ошибка даты"
            return

        night, day = self.shift.get_shift(current_date)
        self.lbl1smena_brigada.text = f"Бригада №{night}"
        self.lbl2smena_brigada.text = f"Бригада №{day}"

        


def main():
    return Shift12H()
