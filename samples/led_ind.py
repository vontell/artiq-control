from artiq.experiment import *

def input_led_state() -> TBool:
    return input("Enter desired LED state: ") == "1"

class LED(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("led")

    @kernel
    def run(self):
        s = input_led_state()
        self.core.break_realtime()
        if s:
            self.led.on()
        else:
            self.led.off()