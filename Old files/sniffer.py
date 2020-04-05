#!/usr/bin/env python3.6
"""
Based on RFC-793, the following figure shows the TCP header format:

0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

In linux api (uapi/linux/tcp.h), it defines the TCP header:

struct tcphdr {
    __be16  source;
    __be16  dest;
    __be32  seq;
    __be32  ack_seq;
#if defined(__LITTLE_ENDIAN_BITFIELD)
    __u16   res1:4,
            doff:4,
            fin:1,
            syn:1,
            rst:1,
            psh:1,
            ack:1,
            urg:1,
            ece:1,
            cwr:1;
#elif defined(__BIG_ENDIAN_BITFIELD)
    __u16   doff:4,
            res1:4,
            cwr:1,
            ece:1,
            urg:1,
            ack:1,
            psh:1,
            rst:1,
            syn:1,
            fin:1;
#else
#error      "Adjust your <asm/byteorder.h> defines"
#endif
    __be16  window;
    __sum16 check;
    __be16  urg_ptr;
};
"""
import sys
import socket
import platform

from struct import unpack
from contextlib import contextmanager

un = platform.system()
if un != "Linux":
    #print(f"{un} is not supported")
    sys.exit(1)

@contextmanager
def create_socket():
    ''' Create a TCP raw socket '''
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_RAW,
                      socket.IPPROTO_TCP)
    try:
        yield s
    finally:
        s.close()


try:
    with create_socket() as s:
        while True:
            pkt, addr = s.recvfrom(65535)

            # the first 20 bytes are ip header
            iphdr = unpack('!BBHHHBBH4s4s', pkt[0:20])
            iplen = (iphdr[0] & 0xf) * 4

            # the next 20 bytes are tcp header
            tcphdr = unpack('!HHLLBBHHH', pkt[iplen:iplen+20])
            source = tcphdr[0]
            dest = tcphdr[1]
            seq = tcphdr[2]
            ack_seq = tcphdr[3]
            dr = tcphdr[4]
            flags = tcphdr[5]
            window = tcphdr[6]
            check = tcphdr[7]
            urg_ptr = tcphdr[8]

            doff = dr >> 4
            fin = flags & 0x01
            syn = flags & 0x02
            rst = flags & 0x04
            psh = flags & 0x08
            ack = flags & 0x10
            urg = flags & 0x20
            ece = flags & 0x40
            cwr = flags & 0x80

            tcplen = (doff) * 4
            h_size = iplen + tcplen

            #get data from the packet
            data = pkt[h_size:]

            if not data:
                continue

            print("------------ TCP_HEADER --------------")
            print("Source Port:           {source}")
            print("Destination Port:      {dest}")
            print("Sequence Number:       {seq}")
            print("Acknowledgment Number: {ack_seq}")
            print("Data offset:           {doff}")
            print("FIN:                   {fin}")
            print("SYN:                   {syn}")
            print("RST:                   {rst}")
            print("PSH:                   {psh}")
            print("ACK:                   {ack}")
            print("URG:                   {urg}")
            print("ECE:                   {ece}")
            print("CWR:                   {cwr}")
            print("Window:                {window}")
            print("Checksum:              {check}")
            print("Urgent Point:          {urg_ptr}")
            print("--------------- DATA -----------------")
            print(data)
            
            raw_input()

except KeyboardInterrupt:
    pass
