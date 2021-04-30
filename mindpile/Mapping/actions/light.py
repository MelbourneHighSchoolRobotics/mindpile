from mindpile.Mapping.utils import MethodCall, Requires, Setup

@Setup
def ledSetup():
    return '''
        import ev3dev2.led
        ledController = ev3dev2.led.Leds()
        ledColours = ["GREEN", "ORANGE", "RED"]
        ledGroups = ["LEFT", "RIGHT"]
        def ledOn(colour, pulse):
            c = ledColours[colour]
            if pulse:
                ledController.animate_flash(c, duration=None, block=False)
            else:
                for g in ledGroups:
                    ledController.set_color(g, c)
    '''

@MethodCall(target="LedOff.vix")
@Requires(ledSetup)
def off():
    return '''
        ledController.all_off()
    '''

@MethodCall(target="LedOn.vix", Color=int, Pulse=bool)
@Requires(ledSetup)
def on():
    return '''
        ledOn(Color, Pulse)
    '''

@MethodCall(target="LedReset.vix")
@Requires(ledSetup)
def reset():
    return '''
        ledController.reset()
    '''
