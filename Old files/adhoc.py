#!/usr/bin/python

# This is the topology used for the routing experiments

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI_wifi
from mininet.node import Controller, RemoteController
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

from positions import positions

def topology(autoTxPower):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='10.0.0.1/8', antennaHeight='1', antennaGain='5', range=800)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='10.0.0.2/8', antennaHeight='1', antennaGain='5', range=800)
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:03', ip='10.0.0.3/8', antennaHeight='1', antennaGain='5', range=800)
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:04', ip='10.0.0.4/8', antennaHeight='1', antennaGain='5', range=800)
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:05', ip='10.0.0.5/8', antennaHeight='1', antennaGain='5', range=800)
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:06', ip='10.0.0.6/8', antennaHeight='1', antennaGain='5', range=800)

    #ap1 = net.addAccessPoint('ap1', ssid='ap1', mode='a', channel='36', position='50,50,0')

    # c0 = net.addController(name='c0',
    #                   controller=InbandController,
    #                   ip='10.0.0.2',
    #                   protocol='tcp',
    #                   port=6653)

    net.setPropagationModel(model="logDistance", exp=5.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    #MANET routing protocols supported by proto: olsr and batman
    net.addLink(sta1, cls=adhoc, ssid='adhocNet', proto='olsr',
                mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta2, cls=adhoc, ssid='adhocNet', proto='olsr',
                mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta3, cls=adhoc, ssid='adhocNet', proto='olsr',
                mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta4, cls=adhoc, ssid='adhocNet', proto='olsr',
                mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta5, cls=adhoc, ssid='adhocNet', proto='olsr',
                mode='g', channel=5, ht_cap='HT40+')
    net.addLink(sta6, cls=adhoc, ssid='adhocNet', proto='olsr',
                mode='g', channel=5, ht_cap='HT40+')

    #net.plotGraph(max_x = 4000, max_y = 2000)

    net.setMobilityModel(time=0, model='RandomWayPoint', max_x=4000, max_y=2000,min_v=5, max_v=20, seed=5)

    info("*** Starting network\n")
    net.build()

    info("*** Addressing...\n")
    sta1.setIPv6('2001::1/64', intf="sta1-wlan0")
    sta2.setIPv6('2001::2/64', intf="sta2-wlan0")
    sta3.setIPv6('2001::3/64', intf="sta3-wlan0")
    sta4.setIPv6('2001::4/64', intf="sta4-wlan0")
    sta5.setIPv6('2001::5/64', intf="sta5-wlan0")
    sta6.setIPv6('2001::6/64', intf="sta6-wlan0")

    nodes = net.stations

    positions(nodes,single=True)

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    autoTxPower = True if '-a' in sys.argv else False
    topology(autoTxPower)
