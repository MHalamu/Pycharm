from IQuackBehavior import IQuackBehavior


class SimpleQuack(IQuackBehavior):

    def quack(self):
        raise Exception("I cannot quack!")
