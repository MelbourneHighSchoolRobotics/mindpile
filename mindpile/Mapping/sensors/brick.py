from mindpile.Mapping.types import List
from mindpile.Mapping.utils import MethodCall, Requires, Setup

# TODO: verify button code works on brick before enabling it

@Setup
def buttonSetup():
    return '''
        import ev3dev2.button
        brickButtons = ev3dev2.button.Button()
        buttonMap = [None, "left", "enter", "right", "up", "down"]
        buttonMapR = { "left": 1, "enter": 2, "right": 3, "up": 4, "down": 5 }
        
        def buttonValue():
            pressed = brickButtons.buttons_pressed
            if len(pressed) == 0:
                return 0
            else:
                return buttonMapR[pressed[0]]
        
        buttonsBumped = [None, False, False, False, False, False]
        buttonsPressedTime = [None, None, None, None, None, None]
        buttonBumpTimeout = 0.5
        def buttonChanged(changedButtons):
            for button, state in changedButtons:
                b = buttonMapR[button]
                if state:
                    buttonsPressedTime[b] = time.time()
                else:
                    if buttonsPressedTime[b] is not None and time.time() <= buttonsPressedTime[b] + buttonBumpTimeout:
                        buttonsBumped[b] = True
                    buttonsPressedTime[b] = None
        brickButtons.on_change = buttonChanged

        def buttonCompare(buttons, action):
            buttonsPressed = brickButtons.buttons_pressed
            for b in buttons:
                button = buttonMap[b]
                if action == 0 and button not in buttonsPressed:
                    return True, b
                elif action == 1 and button in buttonsPressed:
                    return True, b
                elif action == 2 and buttonsBumped[b]:
                    buttonsBumped[b] = False
                    return True, b
            return False, 0
        
        buttonChangeState = None
        buttonNewState = None
    '''

@MethodCall(target="ButtonValue.vix", Value=int)
@Requires(buttonSetup)
def buttonValue():
    return '''
        Value = buttonValue()
    '''

@MethodCall(target="ButtonCompare.vix", Buttons=List(int), Action=int, Result=bool, Value=int)
@Requires(buttonSetup)
def buttonCompare():
    return '''
        Result, Value = buttonCompare(Buttons, Action)
    '''

@MethodCall(target="ButtonChange.vix", Result=bool, Value=int)
@Requires(buttonSetup)
def buttonChange():
    return '''
        if buttonChangeState is None:
            buttonChangeState = set(brickButtons.buttons_pressed)
        buttonNewState = set(brickButtons.buttons_pressed)
        if buttonChangeState != buttonNewState:
            Result = True
            Value = (buttonChangeState ^ buttonNewState).pop()
            buttonChangeState = None
        else:
            Result = False
    '''
