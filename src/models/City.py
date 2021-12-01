import Constants

class City:
    def __init__(self, countryID, name, lat, long):
        self.countryID = countryID
        self.name = name
        self.lat = lat
        self.long = long

def jsonToCity(json):
    countryID = json.get(Constants.COUNTRY_ID)
    if not countryID:
        return None
    name = json.get(Constants.NAME)
    if not name:
        return None
    lat = json.get(Constants.LAT)
    if not lat:
        return None
    long = json.get(Constants.LONG)
    if not long:
        return None
    return City(countryID, name, lat, long)

