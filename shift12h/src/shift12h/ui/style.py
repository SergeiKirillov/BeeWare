from toga.style import Pack
from toga.style.pack import ROW, COLUMN, CENTER

#Стиль главного контейнера
MAIN_STYLE = Pack(
    direction=COLUMN,
    flex=1,
    margin=5,
    align_items=CENTER,
)

#Заголовок
TITLE_STYLE = Pack(
    font_size=16,
    margin_bottom=5, 
)

#Заголовок даты
DATE_TITLE_STYLE = Pack(
    font_size=14,
    margin_bottom=5,
)
#Поле даты
DATE_INPUT_STYLE = Pack(
    flex=1,
    margin=5,
)

#Блок смены
SHIFT_BOX_STYLE = Pack(
    direction=COLUMN,
    flex=1,
    margin=5,
)

#Заголовок смены
SHIFT_TITLE_STYLE = Pack(
    font_size=12,
    margin_bottom=5,
)

#Номер бригады
SHIFT_VALUE_STYLE = Pack(
    font_size=12,
    margin_top=5,
)

#Кнопки
BUTTON_STYLE = Pack(
    flex=1,
    margin=5,
)

#Навигация «До / После»
NAV_BUTTON_STYLE = Pack(
    flex=1,
    margin=5,
)



