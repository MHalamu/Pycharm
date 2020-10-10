from DisplayBehaviors.GraphicDisplay import GraphicDisplay
from FlyBehaviors.JetFly import JetFly
from QuackBehaviors.SimpleQuack import SimpleQuack
from Duck import Duck

my_duck = Duck(
    fly_behavior=JetFly(),
    quack_behavior=SimpleQuack(),
    display_behavior=GraphicDisplay()
)

my_duck.quack()
my_duck.fly()
my_duck.disply()
