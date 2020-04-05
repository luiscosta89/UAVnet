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

class positions(object):
    nodes = []

    def __init__(self, nodes, **kwargs):
        kwargs['nodes'] = nodes
        thread_ = thread(target=self.start, kwargs=(kwargs))
        thread_.daemon = True
        thread_.start()

    def start(self, **kwargs):
        cont = 180

        nodes = kwargs['nodes']

        pos_sta1 = []
        pos_sta2 = []
        pos_sta3 = []
        pos_sta4 = []
        pos_sta5 = []
        pos_sta6 = []

        sta1_x = []
        sta1_y = []

        sta2_x = []
        sta2_y = []

        sta3_x = []
        sta3_y = []

        sta4_x = []
        sta4_y = []

        sta5_x = []
        sta5_y = []

        sta6_x = []
        sta6_y = []

        # Create lists of stations positions
        while (cont > 0):

            pos_sta1.append(nodes[0].params['position'])
            pos_sta2.append(nodes[1].params['position'])
            pos_sta3.append(nodes[2].params['position'])
            pos_sta4.append(nodes[3].params['position'])
            pos_sta5.append(nodes[4].params['position'])
            pos_sta6.append(nodes[5].params['position'])

            time.sleep(20)

            cont = cont - 1

        # Set lists of stations positions
        for item in pos_sta1:
            sta1_x.append(item[0])
            sta1_y.append(item[1])

        for item in pos_sta2:
            sta2_x.append(item[0])
            sta2_y.append(item[1])

        for item in pos_sta3:
            sta3_x.append(item[0])
            sta3_y.append(item[1])

        for item in pos_sta4:
            sta4_x.append(item[0])
            sta4_y.append(item[1])

        for item in pos_sta5:
            sta5_x.append(item[0])
            sta5_y.append(item[1])

        for item in pos_sta6:
            sta6_x.append(item[0])
            sta6_y.append(item[1])

        # Plot graph
        plt.plot(sta1_x, sta1_y, 'k^', label = 'sta1')
        plt.plot(sta2_x, sta2_y, 'k*', label = 'sta2')
        plt.plot(sta3_x, sta3_y, 'ko', label = 'sta3')
        plt.plot(sta4_x, sta4_y, 'ks', label = 'sta4')
        plt.plot(sta5_x, sta5_y, 'k.', label = 'sta5')
        plt.plot(sta6_x, sta6_y, 'kP', label = 'sta6')

        # Add legend
        plt.legend(loc=2, ncol=2)

        plt.show()
