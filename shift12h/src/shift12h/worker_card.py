import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class WorkerCard(toga.Box):
    def __init__(self, worker, **kwargs):
        super().__init__(
            style=Pack(
                direction=COLUMN,
                padding=10,
            ),
            **kwargs
        )
        self.worker = worker

        # Ф.И.О.
        self.fio = toga.Label(
            worker["fio"],
            style=Pack(
                font_size=16,
                padding_bottom=5,
            )
        )

        # Цех
        self.shop = toga.Label(
            f'Цех: {worker["shop"]}',
            style=Pack(
                padding_bottom=3,
            )
        )

        # Должность
        self.position = toga.Label(
            f'Должность: {worker["position"]}',
            style=Pack(
                padding_bottom=3,
            )
        )

        # Телефон
        self.phone = toga.Label(
            f'📞 {worker["phone"]}',
        )

        self.add(self.fio)
        self.add(self.shop)
        self.add(self.position)
        self.add(self.phone)

class BrigadeWindows:
    def __init__(self, app, brigade, workers):
        self.app = app
        self.brigade = brigade
        self.workers = workers

        self.content = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                flex=1,
            )
        )

        self.create_workers()

        self.window = toga.Window(
            title=f"Бригада №{brigade}",
            size=(400, 600),
        )

        self.window.content = self.content

    def create_workers(self):

        for worker in self.workers:

            card = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=10,
                )
            )

            fio = toga.Label(
                worker["fio"],
                style=Pack(
                    font_size=16,
                    padding_bottom=5,
                )
            )

            shop = toga.Label(
                f'Цех: {worker["shop"]}',
                style=Pack(
                    padding_bottom=3,
                )
            )

            position = toga.Label(
                f'Должность: {worker["position"]}',
                style=Pack(
                    padding_bottom=3,
                )
            )

            phone = toga.Button(
                f'📞 {worker["phone"]}',
                on_press=lambda widget, phone=worker["phone"]:
                    self.call_worker(phone),
                style=Pack(
                    padding_top=5,
                )
            )

            card.add(fio)
            card.add(shop)
            card.add(position)
            card.add(phone)

            self.content.add(card)

    def call_worker(self, phone):
        print(f"Звоним: {phone}")

    def show(self):
        self.window.show()