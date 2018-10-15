import sys

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

        self.window.show()
 
    def scan_handler(self):
        output = launch_scanning_network()

        for i in range(len(output)):
            self.output_zone.append(output[i])

    def attack_handler(self):
        target_IP = 'None' if not self.targetIP.text() else self.line.text()
        print('Favorite language: {}'.format(target_IP))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form('GUI.ui')
    sys.exit(app.exec_())