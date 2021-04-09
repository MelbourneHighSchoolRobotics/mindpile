# Mindpile

A transpiler for EV3 mindstorms to ev3dev2 Python.

Using mypy for types and black for code-auto-formatting

## Blocks Not Implemented


## Blocks Partially Implemented

- Display: Doesn't support displaying images, white colour, or text size
- Sound: Doesn't support playing files, repeat play type, or stopping sounds
- Loop Interrupt: Only supports breaking out of a loop it is directly inside. It can't break out more than 1 layer
- Brick Buttons: This probably has some bugs
- Comment: Comments aren't inserted into Python code

## Contributing

Install the package locally with 

    pip install -e  ./
