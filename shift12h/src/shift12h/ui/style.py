from toga.style import Pack
from toga.style.pack import ROW, COLUMN, CENTER


#Pack(direction=COLUMN,margin=16,flex=1)


#Стиль главного контейнера
#style=Pack(direction=COLUMN,margin=20,align_items=CENTER,flex=1)
MAIN_STYLE = Pack(
    direction=COLUMN,
    flex=1,
    margin=5,
    
)

BOX_DATA_SELECT = Pack(
    direction=COLUMN,
    margin=2,
    width=330,
)
BOX_DATA_SELECT_TITLE=Pack(
    direction=ROW,
    margin=2,
    align_items=CENTER,
)
BOX_DATA_SELECT_BUTTON=Pack(
    direction=ROW,
    margin=2,
)
BOX_CONTENT=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)
BOX_CONTENT_DATA=Pack(
    direction=COLUMN,
    margin=2,
    align_items=CENTER,
    
)
BOX_CONTENT_INFO=Pack(
    direction=ROW,
    flex=1,
    margin=2,
)
BOX_CONTENT_INFO_NIGHT=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)
BOX_CONTENT_INFO_DAY=Pack(
    direction=COLUMN,
    flex=1,
    margin=2,
)

BOX_SELECT_DAY_BUTTON=Pack(
    direction=ROW,
    margin=2,
)

#---------------------------------------------------------------------------

# =========================================================
# Элементы
# =========================================================

DATE_INPUT_STYLE = Pack(
    flex=1,
    margin_left=5,
)

BUTTON_STYLE = Pack(
    flex=1,
    margin=5,
)

DATE_TITLE_STYLE = Pack(
    font_size=12,
    margin_right=5,
    
)

SHIFT_TITLE_STYLE = Pack(
    font_size=12,
    margin_bottom=5,
)

SHIFT_VALUE_STYLE = Pack(
    font_size=18,
    margin_top=5,
)




#---------------------------------------------------------------------------







