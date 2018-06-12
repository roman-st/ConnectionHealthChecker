#!/usr/bin/env python

import argparse
import falcon
from ConnectionObserver import ConnectionObserver
from ResourceHandlers import ConnectionResource, ConnectionIdResource
from ConnectionStateStorage import ConnectionStateStorage, ConnectionStorage
from waitress import serve
from threading import Lock

def get_address(args):
    hosts = args.strip().split(":")
    ip, port = hosts[0], int(hosts[1])
    return ip, port

def get_args():
    parser = argparse.ArgumentParser(description='Service for check connection availability')
    parser.add_argument('-s', '--serve', type=str, help='Listen server address', required=True)
    return parser.parse_args().serve

class HealthChecker:
    def __init__(self):
        self._observer = ConnectionObserver()
        self._state = ConnectionStateStorage()
        self._storage = ConnectionStorage()
        self._mutex = Lock()

    def start(self):
        self._observer.start(self._state.SetHostState)

    def stop(self):
        self._observer.stop()

    def addHost(self, ip, port):
        with self._mutex:
            self._storage.addHost(ip, port)
            self._state.addHost(ip, port)
            self._observer.addHost(ip, port)
        
    def deleteHost(self, id):
        with self._mutex:
            ip, port = self._storage.GetHostById(id)
            self._observer.deleteHost(ip, port)
            self._state.deleteHost(ip, port)
            self._storage.deleteHost(id)

    def GetHosts(self):
        with self._mutex:
            return self._storage.GetHosts()

    def GetHostState(self, id):
        with self._mutex:
            ip, port = self._storage.GetHostById(id)
            return self._state.GetHostState(ip, port)

    def FindHostById(self, id):
        with self._mutex:
            if self._storage.GetHostById(id) is None:
                return False
            return True

    def FindHost(self, ip, port):
        with self._mutex:
            if self._storage.GetIdByHost(ip, port) is None:
                return False
            return True

def main():
    healthChecker = HealthChecker()
    connections = ConnectionResource(healthChecker)
    connections_id = ConnectionIdResource(healthChecker)

    api = falcon.API()
    api.add_route('/connections/', connections)
    api.add_route('/connections/add', connections)
    api.add_route('/connections/delete', connections)
    api.add_route('/connections/{connection_id}', connections_id)

    healthChecker.start()

    ip, port = get_address(get_args())
    serve(api, host=ip, port=port)

    healthChecker.stop()

if __name__ == "__main__":
    main()