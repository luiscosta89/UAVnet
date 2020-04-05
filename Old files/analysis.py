#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import os.path
import time
import matplotlib.pyplot as plt

from os import path
from threading import Thread as thread
from mn_wifi.node import AP

class analysis(object):
    nodes = []

    def __init__(self, nodes, **kwargs):
        kwargs['nodes'] = nodes
        thread_ = thread(target=self.start, kwargs=(kwargs))
        thread_.daemon = True
        thread_.start()

    def start(self, **kwargs):
        
        # Traffic starts with half payload and half dummy
        # Set a time and counter to decrease the dummy and increase the payload
        # STA1, STA2, STA3 will be the servers
        # STA4, STA5, STA6 will be the clients
        # It is easier than use threads (remember that this code will already run in thread)
        # Change clients that send payload and dummy
        
