class Duck(object):
    def __init__(self, fly_behavior,
                 quack_behavior, display_behavior):
        self.fly_behavior = fly_behavior
        self.quack_behavior = quack_behavior
        self.display_behavior = display_behavior

    def fly(self):
        self.fly_behavior.fly()

    def quack(self):
        self.quack_behavior.quack()

    def display(self):
        self.display_behavior.display()

