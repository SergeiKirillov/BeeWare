import toga
from datetime import date, datetime

class DateInput(toga.TextInput):
    def __init__(self, **kwargs):
        super().__init__(
            on_change=self.on_date_change,
            **kwargs
            )

    def on_date_change(self, widget):

         #  if not self._updating:
         #       return 
         #  value = self.value

         #  # Оставляем только цифры  
         #  digits = "".join(
         #     char for char in value
         #     if char.isdigit()
         #  )

         #  # Максимум 8 цифр: ДДММГГГГ  
         #  digits= digits[:8]

         #  # Формируем ДД.ММ.ГГГГ
         #  if len(digits) >= 2:
         #     formatted = digits
         #  elif len(digits)<=4:
         #     formatted = digits[:2] + "." + digits[2:]
         #  else:
         #       formatted = digits[:2] + "." + digits[2:4] + "." + digits[4:]

         #  # Если значение действительно изменилось     
         #  if formatted != value:
         #     self._updating = True
         #     try:
         #        self.value = formatted
         #     finally:
         #         self._updating = False
    
         #     # у Toga другой механизм работы с текстовым полем
         pass

             

    def get_date(self):        
         try:
            return datetime.strptime(
                self.value, 
                "%d.%m.%Y"
            ).date()
         except ValueError:
            return None


#[ ]: - при вводе даты и после точки, которая вставляется автоматом, курсор переставляется на одну позицию назад
