from toga.style import Pack
from toga.style.pack import ROW, COLUMN, CENTER


#Pack(direction=COLUMN,margin=16,flex=1)


#Стиль главного контейнера
#style=Pack(direction=COLUMN,margin=20,align_items=CENTER,flex=1)
MAIN_STYLE = Pack(
    direction=COLUMN,
    flex=1,
    margin=5,
    align_items=CENTER,
)

BOX_DATA_SELECT = Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
    align_items = CENTER
)

BOX_DATA_SELECT_TITLE=Pack(
    direction=ROW,
    flex=1,
    margin=2,
)
BOX_DATA_SELECT_BUTTON=Pack(
    direction=ROW,
    flex=1,
    margin=2,
)
BOX_CONTENT=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)

#Pack(direction=ROW, flex=1, align_items=CENTER, margin_bottom=10)
BOX_CONTENT_DATA=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)

BOX_CONTENT_INFO=Pack(
    direction=ROW,
    flex=1,
    margin=2,
)
#Pack(direction=COLUMN,margin=16,flex=1)
BOX_CONTENT_INFO_NIGHT=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)
#Pack(direction=COLUMN,margin=16,flex=1)
BOX_CONTENT_INFO_DAY=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)

BOX_SELECT_DAY_BUTTON=Pack(
    direction=ROW,
    flex=1,
    margin=2,
)

#---------------------------------------------------------------------------

#Навигация «До / После»
#Pack(direction=ROW, align_items=CENTER, margin=(0,10,0,10))
NAV_STYLE = Pack(
    direction=ROW,
    #align_items=CENTER
    flex=1,
    margin=5,
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





