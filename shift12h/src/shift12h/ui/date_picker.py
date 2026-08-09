import toga
import calendar

from datetime import date
from functools import partial

from toga.style import Pack
from toga.style.pack import COLUMN, ROW


MONTHS = [
    "",
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]


WEEKDAYS = [
    "Пн",
    "Вт",
    "Ср",
    "Чт",
    "Пт",
    "Сб",
    "Вс",
]


class DatePicker:

    def __init__(self,app,on_date_selected):

        self.app = app
        self.on_date_selected = on_date_selected

        self.window = None
        self.current_date = date.today()

        self.calendar_box = None
        self.title_label = None

    def show(self, current_date):

        self.current_date = current_date

        self.window = toga.Window(
            title="Выбор даты"
        )

        self.create_interface()

        self.window.show()

    def create_interface(self):

        self.title_label = toga.Label(
            "",
            style=Pack(
                margin=5
            )
        )

        self.calendar_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=10
            )
        )

        main_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                margin=10
            )
        )

        main_box.add(
            self.title_label
        )

        main_box.add(
            self.create_navigation()
        )

        main_box.add(
            self.calendar_box
        )

        cancel_button = toga.Button(
            "Отмена",
            on_press=self.close,
            style=Pack(
                flex=1,
                margin=5
            )
        )

        main_box.add(
            cancel_button
        )

        self.window.content = main_box

        self.update_calendar()

    def create_navigation(self):

        previous_button = toga.Button(
            "←",
            on_press=self.previous_month,
            style=Pack(
                flex=1,
                margin=5
            )
        )

        next_button = toga.Button(
            "→",
            on_press=self.next_month,
            style=Pack(
                flex=1,
                margin=5
            )
        )

        return toga.Box(
            children=[
                previous_button,
                next_button
            ],
            style=Pack(
                direction=ROW
            )
        )

    def previous_month(self, widget):

        if self.current_date.month == 1:

            self.current_date = date(
                self.current_date.year - 1,
                12,
                1
            )

        else:

            self.current_date = date(
                self.current_date.year,
                self.current_date.month - 1,
                1
            )

        self.update_calendar()

    def next_month(self, widget):

        if self.current_date.month == 12:

            self.current_date = date(
                self.current_date.year + 1,
                1,
                1
            )

        else:

            self.current_date = date(
                self.current_date.year,
                self.current_date.month + 1,
                1
            )

        self.update_calendar()

    def update_calendar(self):

        self.title_label.text = (
            f"{MONTHS[self.current_date.month]} "
            f"{self.current_date.year}"
        )

        self.calendar_box.children.clear()

        week_header = toga.Box(
            style=Pack(
                direction=ROW
            )
        )

        for weekday in WEEKDAYS:

            label = toga.Label(
                weekday,
                style=Pack(
                    flex=1,
                    margin=2
                )
            )

            week_header.add(label)

        self.calendar_box.add(
            week_header
        )

        weeks = calendar.monthcalendar(
            self.current_date.year,
            self.current_date.month
        )

        for week in weeks:

            week_box = toga.Box(
                style=Pack(
                    direction=ROW
                )
            )

            for day in week:

                if day == 0:

                    button = toga.Button(
                        "",
                        style=Pack(
                            flex=1,
                            margin=2
                        )
                    )

                    button.enabled = False

                else:

                    button = toga.Button(
                        str(day),
                        on_press=partial(
                            self.select_day,
                            day
                        ),
                        style=Pack(
                            flex=1,
                            margin=2
                        )
                    )

                week_box.add(button)

            self.calendar_box.add(
                week_box
            )

    def select_day(self, day, widget):

        selected_date = date(
            self.current_date.year,
            self.current_date.month,
            day
        )

        self.on_date_selected(
            selected_date
        )

        self.window.close()

    def close(self, widget):

        self.window.close()