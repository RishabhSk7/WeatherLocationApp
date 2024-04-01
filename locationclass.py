class location:
    def __init__(self, key):
        self.manager = key.weather_manager()

    def radial_search(self,coords=[0,0], lim=8):
        a = self.manager.weather_around_coords(coords[0], coords[1], limit=lim)
        for i in a:
            print(i.weather.status)
    
    def box_search(self, coords=[0,0,0,0], zoom=5):
        list = self.manager.weather_at_places_in_bbox(coords[0], coords[1], coords[2],coords[3], zoom=zoom)