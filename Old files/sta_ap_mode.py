#!/usr/bin/python

'This example runs stations in AP mode'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController
from mn_wifi.wmediumdConnector import interference

class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
        return

def topology():
    'Create a network.'
    net = Mininet_wifi(controller=RemoteController, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', ip='192.168.0.1/24')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', ip='192.168.1.1/24')

    ap1 = net.addStation('ap1', mac='02:00:00:00:01:00', ip='192.168.0.10/24')
    ap2 = net.addStation('ap2', mac='02:00:00:00:02:00', ip='192.168.1.10/24')

    c1 = net.addController(name='c1',
                      controller=InbandController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    ap1.setMasterMode(intf='ap1-wlan0', ssid='ap1-ssid', channel='1', mode='n')
    ap2.setMasterMode(intf='ap2-wlan0', ssid='ap2-ssid', channel='6', mode='n')

    info("*** Adding Link\n")
    net.addLink(ap1, ap2)  # wired connection

    info("*** Plotting Graph\n")
    net.plotGraph(max_x=120, max_y=120)

    net.setMobilityModel(time=0, model='RandomWayPoint', max_x=100, max_y=100,min_v=0.5, max_v=2, seed=10)

    info("*** Starting network\n")
    net.build()
    c1.start()

    ap1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    ap2.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    ap1.start([c1])
    ap2.start([c1])

    ap1.setIP('192.168.0.10/24', intf='ap1-wlan0')
    ap1.setIP('192.168.2.1/24', intf='ap1-eth2')
    ap2.setIP('192.168.1.10/24', intf='ap2-wlan0')
    ap2.setIP('192.168.2.2/24', intf='ap2-eth2')
    ap1.cmd('route add -net 192.168.1.0/24 gw 192.168.2.2')
    ap2.cmd('route add -net 192.168.0.0/24 gw 192.168.2.1')
    sta1.cmd('route add -net 192.168.1.0/24 gw 192.168.0.10')
    sta1.cmd('route add -net 192.168.2.0/24 gw 192.168.0.10')
    sta2.cmd('route add -net 192.168.0.0/24 gw 192.168.1.10')
    sta2.cmd('route add -net 192.168.2.0/24 gw 192.168.1.10')

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
