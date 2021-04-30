from mindpile.Mapping.utils import MethodCall, Requires, Setup

# TODO: InvertColor, Size, and images are not supported

@Setup
def displaySetup():
    return '''
        from ev3dev2.display import Display
        import ev3dev2.fonts
        screen = Display()
        screenFont = ev3dev2.fonts.load("charB14")
    '''

@MethodCall(target="DisplayString.vix", Text=str, ClearScreen=bool, X=int, Y=int, InvertColor=bool, Size=int)
@Requires(displaySetup)
def displayStringPixel():
    return '''
        screen.text_pixels(Text, clear_screen=ClearScreen, x=X, y=Y, text_color='black', font=screenFont)
        screen.update()
    '''

@MethodCall(target="DisplayStringGrid.vix", Text=str, ClearScreen=bool, Column=int, Row=int, InvertColor=bool, Size=int)
@Requires(displaySetup)
def displayStringGrid():
    return '''
        screen.text_grid(Text, clear_screen=ClearScreen, x=Column, y=Row, text_color='black', font=screenFont)
        screen.update()
    '''

@MethodCall(target="DisplayLine.vix", ClearScreen=bool, X1=int, Y1=int, X2=int, Y2=int, InvertColor=bool)
@Requires(displaySetup)
def displayLine():
    return '''
        screen.line(clear_screen=ClearScreen, x1=X1, y1=Y1, x2=X2, y2=Y2, line_color='black', width=1)
        screen.update()
    '''

@MethodCall(target="DisplayCircle.vix", ClearScreen=bool, X=int, Y=int, Radius=int, Fill=bool, InvertColor=bool)
@Requires(displaySetup)
def displayCircle():
    return '''
        screen.circle(clear_screen=ClearScreen, x=X, y=Y, radius=Radius, fill_color=(0, 0, 0, 255 if Fill else 0), outline_color='black')
        screen.update()
    '''

@MethodCall(target="DisplayRect.vix", ClearScreen=bool, X=int, Y=int, Width=int, Height=int, Fill=bool, InvertColor=bool)
@Requires(displaySetup)
def displayRect():
    return '''
        screen.rectangle(clear_screen=ClearScreen, x1=X, y1=Y, x2=X+Width, y2=Y+Height, fill_color=(0, 0, 0, 255 if Fill else 0), outline_color='black')
        screen.update()
    '''

@MethodCall(target="DisplayPoint.vix", ClearScreen=bool, X=int, Y=int, InvertColor=bool)
@Requires(displaySetup)
def displayPoint():
    return '''
        screen.point(clear_screen=ClearScreen, x=X, y=Y, point_color='black')
        screen.update()
    '''

@Setup
def displayImageNotImplemented():
    return '''
        print("WARNING: Display Image block is not implemented")
    '''

@MethodCall(target="DisplayFile.vix", Filename=str, ClearScreen=bool, X=int, Y=int)
@Requires(displaySetup)
@Requires(displayImageNotImplemented)
def displayImage():
    return '''
    '''

@MethodCall(target="DisplayClear.vix")
@Requires(displaySetup)
def displayClear():
    return '''
        screen.clear()
    '''
