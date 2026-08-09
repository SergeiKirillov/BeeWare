import toga
from datetime import date
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER


class DatePicker:
    def __init__(self, app, on_date_selected):
        self.app = app
        self.on_date_selected = on_date_selected
        self.window = None

    def show(self, current_date:date):
        self.window = toga.Window(title="Выбор даты", size=(300, 200))
        day_label=toga.Label("День:",style=Pack(margin=5))
        self.day_input = toga.TextInput(value=f"{current_date.day:02d}")
        month_label=toga.Label("Месяц:",style=Pack(margin=5))
        self.month_input = toga.TextInput(value=f"{current_date.month:02d}")
        year_label=toga.Label("Год:",style=Pack(margin=5))
        self.year_input = toga.TextInput(value=f"{current_date.year}")
        cancel_button = toga.Button("Отмена", on_press=self.close, style=Pack(margin=5))
        ok_button = toga.Button("Выбрать", on_press=self.select_date, style=Pack(margin=5))


        window_box = toga.Box(style=Pack(direction=COLUMN, margin=10, alignment=CENTER))

        window_box.add(day_label)
        window_box.add(self.day_input)

        window_box.add(month_label)
        window_box.add(self.month_input)

        window_box.add(year_label)
        window_box.add(self.year_input)

        btn_box = toga.Box(style=Pack(direction=ROW, margin=10, alignment=CENTER))
        btn_box.add(cancel_button)
        btn_box.add(ok_button)

        window_box.add(btn_box)

        self.window.content = window_box
        self.window.show()

    def close(self, widget):
        if self.window:
            self.window.close()
            self.window = None

    def select_date(self, widget):
        try:
            selected_date = date(
                int(self.year_input.value),
                int(self.month_input.value),
                int(self.day_input.value)
            )
            
        except ValueError:
            # Обработка некорректной даты
            self.day_input.value = "Ошибка"
            self.month_input.value = "Ошибка"
            self.year_input.value = "Ошибка"
            self.app.main_window.info_dialog("Ошибка", "Некорректная дата. Пожалуйста, введите правильную дату.")
            return

        
        self.on_date_selected(selected_date)
        self.close(widget)
        