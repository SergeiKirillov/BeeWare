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