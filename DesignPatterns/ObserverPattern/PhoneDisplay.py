from DesignPatterns.ObserverPattern.IObserver import IObserver


class PhoneDisplay(IObserver):

    def __init__(self, observable):
        self.observable = observable
        self.temperature = None

    def update(self):
        print "Executing update on PhoneDisplay"
        self.temperature = self.observable.get_temperature()


