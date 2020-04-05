#!/usr/bin/python

# This is the topology used for the stealth experiments

from __future__ import print_function

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mininet.node import Controller, RemoteController
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

#from positions import positions

def topology():
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference,
                       noise_threshold=-91, fading_coefficient=3)

    info("*** Creating nodes\n")

    sta1 = net.addStation('sta1', position='2000,750,0', antennaHeight='1', antennaGain='10', range='800')
    sta2 = net.addStation('sta2', position='1500,500,0', antennaHeight='1', antennaGain='10', range='800')
    sta3 = net.addStation('sta3', position='1500,1500,0', antennaHeight='1', antennaGain='10', range='800')
    sta4 = net.addStation('sta4', position='2000,1250,0', antennaHeight='1', antennaGain='10', range='800')
    sta5 = net.addStation('sta5', position='2500,1500,0', antennaHeight='1', antennaGain='10', range='800')
    sta6 = net.addStation('sta6', position='2500,500,0', antennaHeight='1', antennaGain='10', range='800')    
    
    # ~ ap1 = net.addAccessPoint('ap1', ssid='ap1', mode='a', channel='36', position='2000,1000,0',range=800)
    
    # ~ c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    #MANET routing protocols supported by proto: olsr and batman
    net.addLink(sta1, cls=adhoc, ssid='sta1', proto='olsr', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta2, cls=adhoc, ssid='sta2', proto='olsr', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta3, cls=adhoc, ssid='sta3', proto='olsr', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta4, cls=adhoc, ssid='sta4', proto='olsr', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta5, cls=adhoc, ssid='sta5', proto='olsr', mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta6, cls=adhoc, ssid='sta6', proto='olsr', mode='g', channel=5, ht_cap='HT40+')

    net.plotGraph(max_x = 4000, max_y = 2000)

    #net.setMobilityModel(time=0, model='RandomWayPoint', max_x=4000, max_y=2000,min_v=5, max_v=20, seed=5)

    info("*** Starting network\n")
    net.build()
    # ~ c1.start()
    # ~ ap1.start([c1])

    info("*** Addressing...\n")

    #STA1
    #sta1.setIP('10.0.1.0/8', intf="sta1-wlan0")
    sta1.setIP('10.0.0.1/8', intf="sta1-wlan0")    

    #STA2
    #sta2.setIP('10.0.2.0/16', intf="sta2-wlan0")
    sta2.setIP('10.0.0.2/8', intf="sta2-wlan0")    

    #STA3
    #sta3.setIP('10.0.3.0/20', intf="sta3-wlan0")
    sta3.setIP('10.0.0.3/8', intf="sta3-wlan0")    

    #STA4
    #sta4.setIP('10.0.4.0/22', intf="sta4-wlan0")
    sta4.setIP('10.0.0.4/8', intf="sta4-wlan0")    

    #STA5
    #sta5.setIP('10.0.5.0/24', intf="sta5-wlan0")
    sta5.setIP('10.0.0.5/8', intf="sta5-wlan0")    

    #STA6
    #sta6.setIP('10.0.6.0/26', intf="sta6-wlan0")
    sta6.setIP('10.0.0.6/8', intf="sta6-wlan0")
   
    #nodes = net.stations

    #positions(nodes,single=True)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
