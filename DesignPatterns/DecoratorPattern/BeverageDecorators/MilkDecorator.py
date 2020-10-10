from AddonDecorator import AddonDecorator


class MilkDecorator(AddonDecorator):

    def __init__(self, beverage):
        self.beverage = beverage

    def cost(self):
        print "In cost() of MilkDecorator."
        return self.beverage.cost() + 5
