#!/usr/bin/env python

from scapy.all import *


def main():
    packets = rdpcap('network100_be557d01b0299a03dd3569893226dda424efc9a0.pcap')

    for p in packets:
        if p['IP'].src == '118.27.110.77':
            # 1	ICMP
            # 6	TCP
            # 17 UDP
            # 50 ESP
            print(p['IP'].proto)


if __name__ == '__main__':
    main()
