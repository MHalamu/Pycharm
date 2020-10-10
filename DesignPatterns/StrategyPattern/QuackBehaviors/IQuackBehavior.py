from abc import ABCMeta, abstractmethod


class IQuackBehavior(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def quack(self):
        pass

