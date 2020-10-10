from abc import ABCMeta, abstractmethod
from DesignPatterns.DecoratorPattern.Beverages.Beverage import Beverage


class AddonDecorator(Beverage):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cost(self):
        pass

