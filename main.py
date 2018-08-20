import numpy as np
import os 
import subprocess
import re 
import utils as util

###
### Python > 3.5
###



LINUX = False
MAC_OS = True

if MAC_OS:
    #Recover network informations needed to execute the MiTM demonstration
    os.system('sudo sysctl -w net.inet.ip.forwarding=1')
    print('IP forwarding update to 1')

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

elif LINUX:
    os.system("sudo echo 1 > '/proc/sys/net/ipv4/ip_forward'")
    print('IP forwarding update to 1')

else:
    raise ValueError('WINDOWS OS not supported.')

