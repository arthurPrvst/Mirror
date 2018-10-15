from scapy.all import sniff, ls, ARP, IPv6, DNS, DNSRR, Ether, conf, IP, send
from subprocess import call
import time
import os

def modify_ip_forwarding(activate=True):
    #Change ip forwarding
    if activate:
        os.system('sudo sysctl -w net.inet.ip.forwarding=1')
        print('Enable IP forwarding')
    else:
        os.system('sudo sysctl -w net.inet.ip.forwarding=0')
        print('Disable IP forwarding')

def hex2bin(d, nb=0):
    # Convert Hexadecimal number to binary
    d=int(d,16)
    if d==0:
        b="0"
    else:
        b=""
        while d!=0:
            b="01"[d&1]+b
            d=d>>1
    return b.zfill(nb)