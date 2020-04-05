#!/usr/bin/python

"""This example shows how to work in adhoc mode

It is a full mesh network

     .sta3.
    .      .
   .        .
sta1 ----- sta4"""

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mininet.node import Controller, RemoteController
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

def topology():
    info("*** Create a network\n")
    net = Mininet_wifi(controller=RemoteController, link=wmediumd,
                       wmediumd_mode=interference,
                       noise_threshold=-91, fading_coefficient=3)

    info("*** Creating nodes\n")

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', antennaHeight='1', antennaGain='5', position='200,200,0', range=100)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8', antennaHeight='1', antennaGain='5', position='200,300,0', range=100)
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.4/8', antennaHeight='1', antennaGain='5', position='200,400,0', range=100)
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.5/8', antennaHeight='1', antennaGain='5', position='400,300,0', range=100)
    sta5 = net.addStation('sta5', mac='00:00:00:00:00:06', ip='10.0.0.6/8', antennaHeight='1', antennaGain='5', position='400,200,0', range=100)
    sta6 = net.addStation('sta6', mac='00:00:00:00:00:07', ip='10.0.0.7/8', antennaHeight='1', antennaGain='5', position='300,200,0', range=100)

    ap1 = net.addAccessPoint('ap1', ssid='ap1', mode='a', channel='36', position='300,300,0',range=100)

    c1 = net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)


    info("*** Configuring Propagation Model\n")

    ## For Log Normal models, use expoents above or equal to 4

    #net.setPropagationModel(model="friis")
    net.setPropagationModel(model="logDistance", exp=4.5)
    #net.setPropagationModel(model="logNormalShadowing", exp=4.5, variance=8)
    #net.setPropagationModel(model="ITU")

    info("*** Configuring wifi nodes\n")

    net.configureWifiNodes()

    info("*** Creating links\n")

    net.addLink(sta1, cls=adhoc, ssid='adhocNet', ht_cap='HT40+')
    net.addLink(sta2, cls=adhoc, ssid='adhocNet', ht_cap='HT40+')
    net.addLink(sta3, cls=adhoc, ssid='adhocNet', ht_cap='HT40+')
    net.addLink(sta4, cls=adhoc, ssid='adhocNet', ht_cap='HT40+')
    net.addLink(sta5, cls=adhoc, ssid='adhocNet', ht_cap='HT40+')
    net.addLink(sta6, cls=adhoc, ssid='adhocNet', ht_cap='HT40+')

    net.addLink(ap1, cls=adhoc, ssid = 'adhocNet')

    net.plotGraph(max_x = 600, max_y = 600)

    info("*** Configuring Mobility Model\n")

    #net.setMobilityModel(time=0, model='RandomWalk', max_x=100, max_y=100,min_v=0.5, max_v=2, seed=10)
    #net.setMobilityModel(time=0, model='RandomWayPoint', max_x=100, max_y=100,min_v=0.5, max_v=2, seed=10)
    #net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, min_v=0.5, max_v=2, seed=10)
    #net.setMobilityModel(time=0, model='GaussMarkov', max_x=100, max_y=100, min_v=0.5, max_v=2, seed=10)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
