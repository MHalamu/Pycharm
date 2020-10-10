from WeatherStation import WeatherStation
from PhoneDisplay import PhoneDisplay
from WindowDisplay import WindowDisplay

weather_station = WeatherStation()

window_display = WindowDisplay(observable=weather_station)
phone_display = PhoneDisplay(observable=weather_station)

weather_station.add(observer=window_display)
weather_station.add(observer=phone_display)

weather_station.notify()


