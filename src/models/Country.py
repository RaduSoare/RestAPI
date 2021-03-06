import Constants
class Country:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def __str__(self):
        print(self.name + " " + str(self.lat) + " " + str(self.long))

def jsonToCountry(json):
    name = json.get(Constants.NAME)
    if not name:
        return None
    lat = json.get(Constants.LAT)
    if not lat:
        return None
    long = json.get(Constants.LONG)
    if not long:
        return None
    return Country(name, lat, long)