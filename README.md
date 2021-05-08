# mindpile

A transpiler for EV3 Mindstorms to ev3dev2 Python.

Using mypy for types and black for code-auto-formatting.

## Using

[ev3sim](https://github.com/MelbourneHighSchoolRobotics/ev3sim) includes native mindpile support, this is the easiest way to get started.

## Blocks Not Implemented


## Blocks Partially Implemented

- Display: Doesn't support displaying images, white colour, or text size
- Sound: Doesn't support playing files, repeat play type, or stopping sounds
- Loop Interrupt: Only supports breaking out of a loop it is directly inside. It can't break out more than 1 layer
- Brick Buttons: This probably has some bugs
- Motor Sensors: You must use a motor from that port before reading the value
- Comment: Comments aren't inserted into Python code

## Contributing

Install the package locally with 

    pip install -e  ./
