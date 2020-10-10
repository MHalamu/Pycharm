from abc import ABCMeta, abstractmethod


class ITarget(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def request(self):
        pass

