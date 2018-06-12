#!/usr/bin/env python
import socket
from threading import Thread
from time import sleep

def ConsoleLogger(ip, port, state):
    print "Ip: {}, port {}: {}".format(ip, port, state)

class ConnectionObserver:
    def __init__(self, updateTime = 0.05, connectionTimeout = 0.1, handler = ConsoleLogger ):
        self._hosts = set()
        self._connectionTimeout = connectionTimeout
        self._updateTime = updateTime
        self._handler = handler
        
    def start(self, handler):
        self._loop = True
        self._handler = handler
        self._thread = Thread(target=self._handle)
        self._thread.start()

    def stop(self):
        self._loop = False
        self._thread.join()

    def addHost(self, ip, port):
        self._hosts.add((ip, port))

    def deleteHost(self, ip, port):
        self._hosts.remove((ip, port))

    def _CheckConnect(self, host):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._connectionTimeout)
            result = sock.connect_ex(host)
            self._handler(host[0], host[1], result == 0)
            sock.close()
        except:
            pass

    def _observe(self):
        for host in self._hosts:
            self._CheckConnect(host)

    def _handle(self):
        while self._loop:
            self._observe()
            sleep(self._updateTime)