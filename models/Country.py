import Constants

class Country:
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long

    def __str__(self):
        print(self.name + " " + str(self.lat) + " " + str(self.long))

def country_to_json(country):
    None