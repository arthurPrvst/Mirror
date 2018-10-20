# Mirror
ARP Poisoning Viewer for local attacks. This tool should be used for educational purpose only. Indeed, even if TLS gives us confidentiality integrity and authentication, it doesn't provide anonimity. One of the possible ways to recover  websites visited by the user (victim) is to do a Man In The Middle (MiTM) attack (with ARP poisonning for example) and then to recover DNS packets.[See how an ARP poisonning attack works](https://www.quora.com/How-does-an-arp-attack-work). 

## How to use it

### How to run the tool

You have to launch the script as ```sudo``` (needed for the scanning phase of the network by the tool).

You have to launch the script as follow :```sudo python main.py```.

### Steps to follow

* First of all, you have to launch a scan of the network in order to get IP adress and MAC adress of the target device. To do so, you have to click on "Scan the network" on the topside of the UI. If you already have these informations, you can skip this step.

* Once IP adress and MAC adress are recovered, fulfill corresponding editText in the bottom left corner. You can now launch ARP Poisonning attack by clicking on "Launch ARP attack".

* Once the attack is launched, domain name recovered from intercepted DNS packets are displayed in the center of the UI.


## How it works

* Scanning phase is done using ```nmap```, and it is not discret at all (not the purpose here). If needed use Syn Scan.

* Arp poisonning is done using ```scapy```. Scapy allows us to craft packet.

* UI is created with PyQt.

## Further informations

* Scan local network : ```nmap -sP ...```

* Forge ARP request packet with scapy : ```send(ARP(op=1, psrc=router_ip, pdst=victim_ip, hwdst=victim_mac))```

## License

This project is licensed under the MIT License.


## Disclaimer

This tool should be used for educational purpose only, in order to prevention. I am not responsible for any evil use of it.
