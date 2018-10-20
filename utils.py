import time
import os

from scapy.all import sniff, ls, ARP, IPv6, DNS, DNSRR, Ether, conf, IP, send
from subprocess import call


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

def check_relevant_packet(info_packet):
    #get DN in the output
    domain_name = info_packet.split(' A ')[-1].split(' ')[0]
    
    #filter relevant DNS packet, and removing those from Content Delivery Network
    # ("www." in domain_name or "m." in domain_name or "blog." in domain_name) and ('cdn.' not in domain_name): 
    if 'cdn.' not in domain_name and 'dns.' not in domain_name: 
        return domain_name
    return False