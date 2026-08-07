"""
Программа для отображение информации о ночной и дневной смене
"""
from .models.session import Session
from datetime import datetime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from toga.style.pack import ROW
from .core.shift import ShiftCalculator



class Shift12H(toga.App):
    def startup(self):

        self.session = Session()

        self.shift = ShiftCalculator()

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        title_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment="center",width=400,height=30))  
        context_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        select_box = toga.Box(style=Pack(direction=ROW, padding=5))

        self.main_window = toga.MainWindow(title=self.formal_name)

        lblData = toga.Label(
            "Дата: ",
            style=Pack(
                padding=(0, 5),
                width=50,
            ),
        )
        self.txtDataSelection= toga.TextInput(
            placeholder="Введите дату",
            style=Pack(
                padding=(0, 5),
                width=100,
                ),
        )
        self.txtDataSelection.on_confirm=self.update_shift
                                   
        self.btnToday=toga.Button(
            "Сегодня",
            on_press=self.btnToday_press,

        )

        self.txtDataSelection.value = "06.08.2026"
        title_box.add(lblData)
        title_box.add(self.txtDataSelection)
        title_box.add(self.btnToday)

        lbl1smena = toga.Label(
            "1 смена: 19:00 - 7:00",
            style=Pack(padding=(0, 5)),
        )
        self.lbl1smena_brigada = toga.Label(
            "_",
            style=Pack(padding=(0, 5)),
        )
        
        
        lbl2smena = toga.Label(
            "2 смена: 7:00 - 19:00",
            style=Pack(padding=(0, 5)),
        )
        self.lbl2smena_brigada = toga.Label(
            "_",
            style=Pack(padding=(0, 5)),
        )
        
        btnDo = toga.Button(
            "До", 
            style=Pack(padding=(0, 5)),
            on_press=self.btnDo_press,
        )
        btnPosle = toga.Button(
            "После", 
            style=Pack(padding=(0, 5)),
            on_press=self.btnPosle_press,
        )
        select_box.add(btnDo)
        select_box.add(btnPosle)


        context_box.add(lbl1smena)
        context_box.add(self.lbl1smena_brigada)
        context_box.add(lbl2smena)  
        context_box.add(self.lbl2smena_brigada)
        context_box.add(select_box)




        main_box.add(title_box)
        main_box.add(context_box)
        self.main_window.content = main_box
        self.main_window.show()

    def btnDo_press(self,widget):
        pass

    def btnPosle_press(self, widget):
        pass

    def btnToday_press(self, widget):
        self.set_today()

    def set_today(self):
        today=datetime.today()
        self.session.current_date = today
        self.txtDataSelection.value = today.strftime("%d.%m.%Y")

    def update_shift(self,widget):
        night, day = self.shift.get_shift(self.session.current_date)
        self.lbl1smena_brigada.text = f"Бригада №{night}"
        self.lbl2smena_brigada.text = f"Бригада №{day}"

        


def main():
    return Shift12H()
