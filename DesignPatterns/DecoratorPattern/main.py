from Beverages.Espresso import Espresso
from BeverageDecorators.MilkDecorator import MilkDecorator
from BeverageDecorators.CarmelDecorator import CarmelDecorator


standard_espresso = Espresso()
print "Cost of standard Espresso: %s" % standard_espresso.cost()

espresso_with_carmel_and_milk = CarmelDecorator(MilkDecorator(Espresso()))
print "Cost of Espresso with carmel and milk: %s" % espresso_with_carmel_and_milk.cost()



################

# Difference between Python Decorators and decorator pattern.

import datetime
import time


class TimeDisplayDecorator(object):

    def __init__(self, func):
        self.func = func

    def __call__(self):
        print "Entering function. Current time is %s" % self.print_time()
        self.func()
        print "Exiting function. Current time is %s" % self.print_time()

    def print_time(self):
        return datetime.datetime.now()


# The act of decoration replaces(!) the original function object with the result of the decoration
@TimeDisplayDecorator  # When executing this line, __init__ of decorator is executed.
def SomeFunction():
    time.sleep(1)
    print("inside SomeFunction()")


print("Finished decorating aFunction()")


SomeFunction()  # Here __call__ from Decorator is executed.