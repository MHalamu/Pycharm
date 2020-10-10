from abc import ABCMeta, abstractmethod


class IObservable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, observer):
        pass

    @abstractmethod
    def remove(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


