import sys
import time 
import os

from threading import Thread
from attack import *
from utils import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QWidget, QTextBrowser
from PySide2.QtCore import QFile, QObject

class ReaderThread(Thread):
    def __init__(self, readerProcess, zone):
        Thread.__init__(self)
        self.p = readerProcess
        self.result_zone = zone
        self.last_domain_name = ''
        self.daemon = True
        self.running = True

    def run(self):

        while self.running:
            output = self.p.stdout.readline()

            if output == '' and self.p.poll() is not None:
                break
            if output:
                output = output.decode('utf-8')
                domain_name = check_relevant_packet(output)
                if domain_name and (domain_name != self.last_domain_name):
                    self.result_zone.append(domain_name)
                    self.last_domain_name = domain_name
        rc = self.p.poll()

    def stop(self):
        self.running = False