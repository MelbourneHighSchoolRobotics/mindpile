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
'''
