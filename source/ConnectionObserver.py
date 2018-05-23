#!/usr/bin/env python
import socket
import threading

def ConsoleLogger(ip, port, state):
    print "Ip: {}, port {}: {}".format(ip, port, state)

class ConnectionObserver:
    def __init__(self, hosts, handler = ConsoleLogger, timeout=0.1):
        self._hosts = hosts
        self._timeout = timeout
        self._handler = handler
        
    def start(self, handler):
        self._loop = True
        self._handler = handler
        self._thread = threading.Thread(target=self._handle)
        self._thread.start()

    def stop(self):
        self._loop = False
        self._thread.join()

    def _observe(self):
        for host in self._hosts:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self._timeout)
                result = sock.connect_ex(host)
                self._handler(host[0], host[1], result == 0)
                sock.close()
            except:
                pass

    def _handle(self):
        while self._loop:
            self._observe()