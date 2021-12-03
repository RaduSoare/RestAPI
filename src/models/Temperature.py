import Constants
from datetime import datetime, timezone

class Temperature:
    def __init__(self, cityID, value):
        self.cityID = cityID
        self.value = value
        self.timestamp = datetime.now(timezone.utc)

def jsonToTemperature(json):
    cityID = json.get(Constants.CITY_ID)
    if not cityID:
        return None
    value = json.get(Constants.VALUE)
    if not value:
        return None
    return Temperature(cityID, value)

