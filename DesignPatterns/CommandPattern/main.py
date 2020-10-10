from invoker import Invoker, InvokerGeneral
from commands import LightOffCommand, LightOnCommand
from light_bulb import LightBulb

light_bulb = LightBulb

light_invoker = Invoker(
    light_on_command=LightOnCommand(light_bulb),
    light_off_command=LightOffCommand(light_bulb))

light_invoker.on_button()
light_invoker.off_button()

# -------------------------

general_invoker = InvokerGeneral()
general_invoker.set_command(LightOnCommand.CMD_NAME, LightOnCommand(light_bulb))
general_invoker.set_command(LightOffCommand.CMD_NAME, LightOffCommand(light_bulb))

general_invoker.execute(LightOnCommand.CMD_NAME)
general_invoker.execute(LightOffCommand.CMD_NAME)
