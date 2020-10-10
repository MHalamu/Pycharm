from abc import ABCMeta, abstractmethod


class IDisplayBehavior(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def display(self):
        pass

