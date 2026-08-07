from datetime import date, datetime
from shift12h.models.session import Session

class ShiftCalculator:
    def __init__(self):
        #Начало отсчёта
        self.base_date=datetime.strptime("01.01.2026", "%d.%m.%Y").date()

        #Цикл смен
        #1 - Алексей Талах - Зарина Алироева
        #2 - Вадим -
        #3 - Серега Волков - Татьяна
        #4 - Алпамыс Кулбаев - Лариса Саталкина
        self.cycle=[
            {"night": 2, "day": 4},
            {"night": 1, "day": 3},
            {"night": 4, "day": 2},
            {"night": 3, "day": 1},
        ]

    def get_shift(self, date_value):
        """
        date_value может быть строкой '31.07.2026'
        или объектом date
        
        Возвращает:
        (ночная_бригада, дневная_бригада)
        """
        #date_value=Session.current_date


        if isinstance(date_value, str): #принятое значение является строкой
            date_value = datetime.strptime(date_value, "%d.%m.%Y").date() # преобразуем её к типу date

        #отнимаем от тек даты - базовую дату и получаем значение дней 
        days = (date_value - self.base_date).days

        #
        row = self.cycle[days%len(self.cycle)]

       #
       # return Shift(
       #     date=date_value,
       #     night=row["night"],
       #     day=row["day"]
       # )
        return row["night"], row["day"]

#      def get_shift(self, current_date):
#    
#
#      return 2,4