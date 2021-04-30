from mindpile.Mapping.utils import MethodCall, Requires, Setup

# TODO: implement playing files, non-blocking looping playtype, stopping sound once there's support in ev3dev

@Setup
def soundSetup():
    return '''
        from ev3dev2.sound import Sound
        speaker = Sound()
    '''

@Setup
def soundStopNotImplemented():
    return '''
        print("WARNING: Stop Sound is not implemented")
    '''

@MethodCall(target="PlaySoundStop.vix")
@Requires(soundSetup)
@Requires(soundStopNotImplemented)
def soundStop():
    return '''
    '''

@Setup
def soundFileNotImplemented():
    return '''
        print("WARNING: Play Sound File is not implemented")
    '''

@MethodCall(target="PlaySoundFile.vix")
@Requires(soundSetup)
@Requires(soundFileNotImplemented)
def soundFile():
    return '''
    '''

@MethodCall(target="PlayTone.vix", Frequency=float, Duration=float, Volume=int, PlayType=int)
@Requires(soundSetup)
def soundTone():
    return '''
        speaker.play_tone(frequency=Frequency, duration=Duration, volume=Volume, play_type=PlayType)
    '''

@MethodCall(target="PlayNote.vix", Note=str, Duration=float, Volume=int, PlayType=int)
@Requires(soundSetup)
def soundNote():
    return '''
        speaker.play_note(note=Note, duration=Duration, volume=Volume, play_type=PlayType)
    '''
