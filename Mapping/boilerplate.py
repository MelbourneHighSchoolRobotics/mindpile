boilerplate = '''
import math
import random
import time

devices = {}
def d(port, type=None):
    m = devices.get(port)
    if m is None:
        if type is None:
            raise Exception(f"Can't create device {port} without type")
        m = type(address=port)
        devices[port] = m
    return m
'''
