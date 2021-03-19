boilerplate = '''
import math
import random
import time

motors = {}
def m(port, type=None):
    if port is None:
        raise Exception("Motor block does not have a port specified")
    port = int(port)

    motor = motors.get(port)
    if motor is None:
        if type is None:
            portName = f"out{chr(port+64)}"
            raise Exception(f"Can't use motor {portName} without knowing its type")
        motor = type(address=portName)
        motors[port] = motor
    return motor

sensors = {}
def s(port, type=None):
    if port is None:
        raise Exception("Sensor block does not have a port specified")
    port = int(port)

    sensor = sensors.get(portName)
    if sensor is None:
        portName = f"in{chr(port+48)}"
        if type is None:
            raise Exception(f"Can't use sensor {portName} without knowing its type")
        sensor = type(address=portName)
        sensors[portName] = sensor
    return sensor

def compare(comparison, a, b):
    if comparison == 0:
        return math.isclose(a, b)
    elif comparison == 1:
        return not math.isclose(a, b)
    elif comparison == 2:
        return a > b
    elif comparison == 3:
        return a >= b
    elif comparison == 4:
        return a < b
    elif comparison == 5:
        return a <= b
    return False

def compareDirection(direction, amount, a, b):
    if direction == 0:
        return b >= a + amount
    elif direction == 1:
        return b <= a - amount
    elif direction == 2:
        return (b >= a + amount) or (b <= a - amount)
    return False
'''
