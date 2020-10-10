from abc import ABCMeta, abstractmethod


class IObserver(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        pass

