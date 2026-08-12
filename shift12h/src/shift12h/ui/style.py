from toga.style import Pack
from toga.style.pack import ROW, COLUMN, CENTER


#Pack(direction=COLUMN,margin=16,flex=1)


#Стиль главного контейнера
#style=Pack(direction=COLUMN,margin=20,align_items=CENTER,flex=1)
MAIN_STYLE = Pack(
    direction=COLUMN,
    # v1    
    #flex=1,
    #margin=5,
    # v2
    #padding=15,
    margin=15,
    gap = 10,
)

BOX_DATA_SELECT = Pack(
    direction=COLUMN,
    #v1
    # margin=2,
    # width=330,
    #v3
    gap=10,
)
BOX_DATA_SELECT_TITLE=Pack(
    direction=ROW,
    # v1
    #margin=2,
    #align_items=CENTER,
    # v2
    gap=10,

)

#кнопки даты
BOX_DATA_SELECT_BUTTON=Pack(
    direction=ROW,
    # V1
    # margin=2,
    #v3
    gap=10,
)
# =========================================================
# Информация о сменах
# =========================================================

BOX_CONTENT=Pack(
    direction=COLUMN,
    # v1
    # flex=1,
    # margin=2,
    #v3
    gap=5,
    margin=2,
)
BOX_CONTENT_DATA=Pack(
    direction=COLUMN,
    margin=2,
    # v1
    # align_items=CENTER,
    
)
BOX_CONTENT_INFO=Pack(
    direction=COLUMN,
    # v1
    # flex=1,
    margin=2,
    # v3
    gap=5,
)
BOX_CONTENT_INFO_NIGHT=Pack(
    direction=COLUMN,
    # v1 
    # flex=1,
    # margin=2,
    # v2
    #padding_top = 5,
    #padding_bottom = 5,
    margin_top = 5,
    margin_bottom = 5,
)
BOX_CONTENT_INFO_DAY=Pack(
    direction=COLUMN,
    # v1 
    # flex=1,
    # margin=2,
    # v2
    #padding_top = 5,
    #padding_bottom = 5,
    margin_top = 5,
    margin_bottom = 5,
)
# =========================================================
# Кнопки До / После
# =========================================================

BOX_SELECT_DAY_BUTTON=Pack(
    direction=ROW,
    # v1 
    # margin=2,
    # v2
    gap = 10,
    #padding_top = 10,
    margin_top = 10,

)

#---------------------------------------------------------------------------

# =========================================================
# Элементы
# =========================================================


DATE_TITLE_STYLE = Pack(
    font_size=12,
    # v1 
    #margin_right=5,   
    # v2
    #padding_top=8,
    margin_top=8,
)

DATE_INPUT_STYLE = Pack(
    flex=1,
    # v1
    #margin_left=5,
)   

BUTTON_STYLE = Pack(
    flex=1,
    # v1
    # margin=5,
    # v2
    #padding = 10,
    margin = 10,
)


SHIFT_TITLE_STYLE = Pack(
    # v1
    # font_size=12,
    # margin_bottom=5,
    # v2
    font_size=16,
)

SHIFT_VALUE_STYLE = Pack(
    # v1
    # font_size=18,
    # margin_top=5,
    # v2
    font_size=26,
    #padding_top=3,
    margin_top=3,
)




#---------------------------------------------------------------------------







