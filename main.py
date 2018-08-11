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
    os.system('sudo sysctl -w net.inet.ip.forwarding=1')
    print('IP forwarding update to 1')

    ifconfig_process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
    grep_process = subprocess.run(['grep', 'inet 192.168.'], stdin=ifconfig_process.stdout, stdout=subprocess.PIPE)
    our_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', str(grep_process.stdout))[0]
    netmask = re.findall(r'([0-9a-fA-Fx]{10})', str(grep_process.stdout))
    netmask = ''.join(netmask)
    netmask = netmask[2:]
    binary_mask = util.hex2bin(netmask)
    print('Your local ip address : '+str(our_ip))
    print('Subnetwork mask : '+str(binary_mask))
    
elif LINUX:
    os.system("sudo echo 1 > '/proc/sys/net/ipv4/ip_forward'")
else:
    raise ValueError('WINDOWS OS not supported.')

