from adapter import Adapter
from adaptee import Adaptee


target = Adapter(adaptee=Adaptee())
target.request()

