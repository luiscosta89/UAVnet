#!/usr/bin/python

from time import sleep
import os

from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mn_wifi.cli import CLI_wifi
from mn_wifi.node import OVSAP
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, mesh
from mininet.term import makeTerm, cleanUpScreens
from mn_wifi.wmediumdConnector import interference
from mn_wifi.sumo.runner import sumo


class InbandController( RemoteController ):

    def checkListening( self ):
        "Overridden to do nothing."
        return

def topology():

    os.system('sudo fuser -k 6653/tcp')
    os.system('sudo fuser -k 6690/tcp')
    os.system('sudo fuser -k 6691/tcp')
    os.system('systemctl stop firewalld')
    os.system('service network-manager stop')

    "Create a network."
    net = Mininet_wifi(controller=InbandController,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       accessPoint=OVSAP,
                       )

    ip_c0 = '10.0.0.101'
    ip_c1 = '10.0.0.102'
    ip_c2 = '10.0.0.103'

    info("*** Creating nodes\n")
    cars = []
    for id in range(0, 10):
        cars.append(net.addCar('car%s' % (id+1), wlans=2, encrypt='wpa2,'))
        #cars.append(net.addCar('car%s' % (id+1), wlans=2, passwd='123456789a,123456789a', encrypt='wpa2,wpa2'))

    enb1 = net.addAccessPoint('enb1', mac='00:00:00:00:00:01', ssid="handover",
                              mode="g", channel="1", datapath='user',
                              passwd='123456789a', encrypt='wpa2',
                              mobility_domain='a1b2',
                              dpid='1', position='3279.02,3736.27,0',
                              inband=True)
    enb2 = net.addAccessPoint('enb2', mac='00:00:00:00:00:02', ssid="handover",
                              mode="g", channel="6", datapath='user',
                              passwd='123456789a', encrypt='wpa2',
                              mobility_domain='a1b2',
                              dpid='2', position='2320.82,3565.75,0', color='r',
                              inband=True)
    enb3 = net.addAccessPoint('enb3', mac='00:00:00:00:00:03', ssid="handover",
                              mode="g", channel="11", datapath='user',
                              passwd='123456789a', encrypt='wpa2',
                              mobility_domain='a1b2',
                              dpid='3', position='2806.42,3395.22,0',
                              inband=True)
    # backbone1 = net.addSwitch('backbone1', mac='00:00:00:00:00:04', dpid='4',
    #                          failMode='standalone')
    h1 = net.addHost('h1', ip=ip_c0)
    h2 = net.addHost('h2', ip=ip_c1)
    h3 = net.addHost('h3', ip=ip_c2)
    server1 = net.addHost('server1', ip='10.0.0.100/8')
    c0 = net.addController('c0', controller=InbandController, port=6653, ip=ip_c0)
    c1 = net.addController('c1', controller=InbandController, port=6690, ip=ip_c1)
    c2 = net.addController('c2', controller=InbandController, port=6691, ip=ip_c2)

    net.setPropagationModel(model="logDistance", exp=2)
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    info("*** Associating Stations\n")
    # net.addLink(backbone1, enb1)
    # net.addLink(backbone1, enb2)
    # net.addLink(backbone1, enb3)
    # net.addLink(backbone1, server1)
    net.addLink(h1, enb1)
    net.addLink(h2, enb2)
    net.addLink(h3, enb3)

    #net.plotGraph(max_x=200, max_y=200)
    net.useExternalProgram(program=sumo, port=8813,
                           config_file='map.sumocfg')

    net.setBgscan(signal=-60, s_inverval=5, l_interval=10)

    info("*** Starting network\n")
    net.build()
    #net.addNAT().configDefault()
    enb1.start([c0])
    enb2.start([c1])
    enb3.start([c2])
    # backbone1.start([])

    sleep(3)


    enb1.cmdPrint('sysctl net.ipv4.ip_forward=1')
    enb2.cmdPrint('sysctl net.ipv4.ip_forward=1')
    enb3.cmdPrint('sysctl net.ipv4.ip_forward=1')

    enb1.cmdPrint('ifconfig enb1-eth2 10.0.0.201')
    enb2.cmdPrint('ifconfig enb2-eth2 10.0.0.202')
    enb3.cmdPrint('ifconfig enb3-eth2 10.0.0.203')

    enb1.cmD('route add 10.0.0.101 dev enb1-eth2')
    enb2.cmd('route add 10.0.0.102 dev enb2-eth2')
    enb3.cmd('route add 10.0.0.103 dev enb3-eth2')


    cars[0].cmd('iw dev %s-wlan0 interface '
                'add %s-mon0 type monitor'
                % (cars[0].name, cars[0].name))
    cars[0].cmd('ifconfig %s-mon0 up' % cars[0].name)
    cars[0].cmd('ifconfig %s-wlan0 10.0.0.1' % cars[0].name)
    cars[0].cmd('route add default gw 10.0.0.12')
    cars[0].cmd('ifconfig lo up')


    #enb1.cmdPrint('dpctl unix:/tmp/enb1 flow-mod table=0,cmd=add in_port=1,eth_type=0x800,ip_proto=17,udp_src=8000 apply:output=ctrl')
    #enb2.cmdPrint('dpctl unix:/tmp/enb2 flow-mod table=0,cmd=add in_port=1,eth_type=0x800,ip_proto=17,udp_src=8000 apply:output=ctrl')
    #enb1.cmdPrint('dpctl unix:/tmp/enb1 flow-mod table=0,cmd=add in_port=1,ip_proto=17,udp_src=8000 apply:output=ctrl')
    #enb2.cmdPrint('dpctl unix:/tmp/enb2 flow-mod table=0,cmd=add in_port=1,ip_proto=17,udp_src=8000 apply:output=ctrl')
    #enb3.cmdPrint('dpctl unix:/tmp/enb3 flow-mod table=0,cmd=add in_port=1,ip_proto=17,udp_src=8000 apply:output=ctrl')
    #enb1.cmdPrint('dpctl unix:/tmp/enb1 flow-mod table=0,cmd=add in_port=2,ip_proto=17,udp_dst=8000 apply:output=1')
    #enb2.cmdPrint('dpctl unix:/tmp/enb2 flow-mod table=0,cmd=add in_port=2,ip_proto=17,udp_dst=8000 apply:output=1')
    #enb3.cmdPrint('dpctl unix:/tmp/enb3 flow-mod table=0,cmd=add in_port=2,ip_proto=17,udp_dst=8000 apply:output=1')
    #enb1.cmd('ovs-ofctl add-flow "enb1" in_port=1,udp,tp_src=8000,actions=controller')
    #enb2.cmd('ovs-ofctl add-flow "enb2" in_port=1,udp,tp_src=8000,actions=controller')
    #enb3.cmd('ovs-ofctl add-flow "enb3" in_port=1,udp,tp_src=8000,actions=controller')
    #makeTerm(cars[0], cmd="bash -c 'ping 10.0.0.100 -c200 > ping.txt;'")
    makeTerm(h1, cmd="bash -c 'cd ryu && ./test.sh h1;'")
    makeTerm(h2, cmd="bash -c 'cd ryu && ./test.sh h2;'")
    makeTerm(h3, cmd="bash -c 'cd ryu && ./test.sh h3;'")
    cars[0].cmd(' python %s.py &' % cars[0].name)

    info("*** Running CLI\n")
    CLI_wifi(net)

    os.system('pkill -f \"xterm -title\"')
    os.system('pkill sumo-gui')
    os.system('pkill ryu-manager')

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
