import toga
from datetime import date, datetime

class DateInput(toga.TextInput):
    def __init__(self, **kwargs):
        super().__init__(
            on_change=self.on_date_change,
            **kwargs
            )

    def on_date_change(self, widget):

        value = self.value

        digits = "".join(
             char for char in value
             if char.isdigit()
        )

        digits= digits[:8]

        parts=[]

        if len(digits) >= 2:
             parts.append(digits[:2])
        else:
             parts.append(digits)

        if len(digits)>=4:
             parts.append(digits[2:4])
        elif len(digits)>2:
             parts.append(digits[2:])

        if len(digits)>4:
             parts.append(digits[4:])

        formatted=".".join(parts)

        if formatted != value:
             self.value = formatted


    def get_date(self):        
         try:
            return datetime.strptime(
                self.value, 
                "%d.%m.%Y"
            ).date()
         except ValueError:
            return None


#[ ]: - при вводе даты и после точки, которая вставляется автоматом, курсор переставляется на одну позицию назад
