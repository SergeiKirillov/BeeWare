from dataclasses import dataclass
from datetime import date


@dataclass
class Session:
    #current_date:date | None= None
    current_date:date=date.today()
    night_shift:int =0 
    day_shift:int = 0 

