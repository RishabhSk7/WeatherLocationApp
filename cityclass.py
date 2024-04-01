
class city:
    def __init__(self, key, closest, url):
        self.city_id = closest[0]
        self.name = closest[1]
        self.country = closest[2]
        self.state = closest[3]
        self.lat = closest[4]
        self.lon = closest[5]
        self.manager = key.weather_manager()
        self.air_manager = key.airpollution_manager()
        self.observation = self.manager.weather_at_place(f"{self.name},{self.country}")

        self.url = url

    def current_weather(self):
        return self.observation.weather.status
    
    def today_temprature(self, unit="celsius"):
        if unit.lower() in ("celsius", "kelvin", "fahrenheit"):
            temprature = self.observation.weather.temperature(unit)
        else:
            print("Wrong input.")
            return 0
        return temprature['temp_min']+temprature['temp_max']


    def current_wind(self):
        wind = self.observation.weather.wind()
        return wind
    
    def current_rain(self):
        rain = self.observation.weather.rain    #Get current rain amount on a location in mms, and none if no rain is there
        return rain

    def visibility(self):
        visibility = self.observation.weather.visibility_distance
        return visibility

    def sun_timings(self):
        return [str(self.observation.weather.sunrise_time("iso"))[:-6]+"UTC", str(self.observation.weather.sunset_time("iso"))[:-6]+"UTC"]


    #PAID    
    """def weather_day_forecast(self):
        one_call = self.manager.one_call(lat=52.5244, lon=13.4105)

        print(one_call.forecast_daily[0].temperature('celsius').get('feels_like_morn', None)) """
    
    def air_pollutants(self):
        air_status = self.air_manager.air_quality_at_coords(self.lat,self.lon)
        print(air_status)
        try:
            return [air_status.co, air_status.no, air_status.no2, air_status.o3, air_status.so2, air_status.pm2_5, air_status.pm10, air_status.nh3]
        except:
            return ["n/a","n/a","n/a","n/a","n/a","n/a","n/a","n/a"]
        
    def air_quality(self, element=None):
        print(self.air_manager.air_quality_at_place(self.lat,self.lon).aqi)

    