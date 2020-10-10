from abc import ABCMeta, abstractmethod


class ICommand(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def unexecute(self):
        pass
