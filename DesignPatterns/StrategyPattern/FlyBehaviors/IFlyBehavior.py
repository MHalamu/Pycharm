from abc import ABCMeta, abstractmethod


class IFlyBehavior(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fly(self):
        pass

