from exceptions import NegativeTitlesError, ImpossibleTitlesError, InvalidYearCupError
from datetime import datetime


def data_processing(data: dict):
    if data["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    
    first_cup = int(data['first_cup'].split('-')[0])

    if first_cup < 1930 or not first_cup % 4 == 2:
        raise InvalidYearCupError("there was no world cup this year")
    
    actual_date = datetime.now().year
    first_cup = int(data['first_cup'].split('-')[0])
    
    if data["titles"] * 4 > (actual_date - first_cup):
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
    
    return data
    
    



