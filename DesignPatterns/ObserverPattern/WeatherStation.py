from DesignPatterns.ObserverPattern.IObservable import IObservable
from random import randint


class WeatherStation(IObservable):

    def __init__(self):
        self.list_of_observers = []

    def add(self, observer):
        self.list_of_observers.append(observer)

    def remove(self, observer):
        self.list_of_observers.remove(observer)

    def notify(self):
        print "Executing notify on WeatherStation\n"
        for observer in self.list_of_observers:
            observer.update()

    @staticmethod
    def get_temperature():
        temperature = randint(1, 100)
        print "Getting temp %s from Station" % temperature
        return temperature

