from AddonDecorator import AddonDecorator


class CarmelDecorator(AddonDecorator):

    def __init__(self, beverage):
        self.beverage = beverage

    def cost(self):
        print "In cost() of CarmelDecorator."
        return self.beverage.cost() + 2

