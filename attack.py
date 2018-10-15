import numpy as np
import os 
import subprocess
import re 
import utils as util

###
### Python > 3.5
###


def launch_scanning_network(MAC_OS=True):
    LINUX = False
    MAC_OS = True

    if MAC_OS:
        #Recover network informations needed to execute the MiTM demonstration

        util.modify_ip_forwarding(activate=True)

        print('----- '+str('Network Info')+' -----')
        ifconfig_process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
        grep_process = subprocess.run(['grep', 'inet 192.168.'], stdin=ifconfig_process.stdout, stdout=subprocess.PIPE)
        our_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(grep_process.stdout))[0]
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
        print('Route IP : '+str(route_ip))

        print('----- '+str('Scanning Network')+' -----')
        route_ip_ends_0 = ''.join([route_ip[:-2], '.'])
        route_ip_ends_0 = route_ip_ends_0 + str(0) + str('/') + str(mask_length)
        os.system('sudo nmap -sP '+str(route_ip_ends_0))
        print('---------------------')
        #nmap scan report ; Host is up ; MAC adress
        #ip.src == 192.168.0.16 and (udp.port == 53 || tcp.port == 53)

    elif LINUX:
        os.system("sudo echo 1 > '/proc/sys/net/ipv4/ip_forward'")
        print('IP forwarding update to 1')

    else:
        raise ValueError('WINDOWS OS not supported.')
    return "ok"
    
def launch_attack():
    #Launch ARP Poisoning
    util.arp_mitm_attack()


