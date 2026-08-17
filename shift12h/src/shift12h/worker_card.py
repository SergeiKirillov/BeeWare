import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class WorkerCard(toga.Box):
    def __init__(self, worker, **kwargs):
        super().__init__(
            style=Pack(
                direction=COLUMN,
                # v1
                # padding=10,
                margin = 10,
            ),
            **kwargs
        )
        self.worker = worker

        # Ф.И.О.
        self.fio = toga.Label(
            worker["fio"],
            style=Pack(
                font_size=16,
                # v1
                # padding_bottom=5,
                # v2 
                margin_bottom=5
            )
        )

        # Цех
        self.shop = toga.Label(
            f'Цех: {worker["shop"]}',
            style=Pack(
                # v1 
                # padding_bottom=3,
                # v2
                margin_bottom=3
            )
        )

        # Должность
        self.position = toga.Label(
            f'Должность: {worker["position"]}',
            style=Pack(
                # v1 
                # padding_bottom=3,
                # v2
                margin_bottom=3

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
                # v1 
                # padding=10,
                margin = 10,
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
                    #v1 
                    # padding=10,
                    # v2
                    margin=10
                )
            )

            fio = toga.Label(
                worker["fio"],
                style=Pack(
                    font_size=16,
                    # v1 
                    # padding_bottom=5,
                    # v2
                    margin_bottom = 5,
                )
            )

            shop = toga.Label(
                f'Цех: {worker["shop"]}',
                style=Pack(
                    #v1 
                    # padding_bottom=3,
                    #v2
                    margin_bottom=3
                )
            )

            position = toga.Label(
                f'Должность: {worker["position"]}',
                style=Pack(
                    # v1
                    # padding_bottom=3,
                    # v2
                    margin_bottom=3
                )
            )

            phone = toga.Button(
                f'📞 {worker["phone"]}',
                on_press=lambda widget, phone=worker["phone"]:
                    self.call_worker(phone),
                style=Pack(
                    # v1 
                    # padding_top=5,
                    margin_top=5

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

class BrigadeWindows2:
    def __init__(self, app, brigade, workers):
        self.app = app
        self.brigade = brigade
        self.workers = workers

        self.content = toga.Box(
            style=Pack(
                direction=COLUMN,
                # v1 
                # padding=10,
                margin = 10,
                flex=1,
            )
        )
        self.create_workers()

        # Возвращаемое значение
        # self.content

    def create_workers(self):
        for worker in self.workers:
            card = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    #v1 
                    # padding=10,
                    # v2
                    margin=10
                )
            )

            fio = toga.Label(
                worker["fio"],
                style=Pack(
                    font_size=16,
                    # v1 
                    # padding_bottom=5,
                    # v2
                    margin_bottom = 5,
                )
            )

            shop = toga.Label(
                f'Цех: {worker["shop"]}',
                style=Pack(
                    #v1 
                    # padding_bottom=3,
                    #v2
                    margin_bottom=3
                )
            )

            position = toga.Label(
                f'Должность: {worker["position"]}',
                style=Pack(
                    # v1
                    # padding_bottom=3,
                    # v2
                    margin_bottom=3
                )
            )

            phone = toga.Button(
                f'📞 {worker["phone"]}',
#                on_press=lambda widget, phone=worker["phone"]:
#                    self.call_worker(phone),
                style=Pack(
                    # v1 
                    # padding_top=5,
                    margin_top=5

                )
            )

            card.add(fio)
            card.add(shop)
            card.add(position)
            card.add(phone)

            self.content.add(card)
        

    # def call_worker(self, phone):
    #     print(f"Звоним: {phone}")

    # def show(self):
    #     self.window.show()