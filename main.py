#!/usr/bin/env python

import falcon
from ConnectionObserver import ConnectionObserver
from ResourceHandlers import ConnectionResource, ConnectionIdResource
from waitress import serve

class HostStateStorage:
    def __init__(self, hosts):
        self._states = {} # (ip, port) = state
        self._ids = {} # id = (ip, port)

        id = 0
        for host in hosts:
            self._ids[id] = host
            id += 1

    def GetHosts(self):
        return self._ids.items()

    def SetHostState(self, ip, port, state):
        self._states[(ip, port)] = state

    def GetHostState(self, id):
        key = self._ids.get(id)
        if not key in self._states:
            return (key[0], key[1], False)
        return (key[0], key[1], self._states[key])

    def FindHost(self, id):
        return id in self._ids.keys()

def main():
    ip = ("192.168.0.100", "192.168.1.145")

    hosts = []
    for port in range(40000, 45000):
        hosts.append((ip[0], port))
        #hosts.append((ip[1], port))

    storage = HostStateStorage(hosts)

    observer = ConnectionObserver(hosts)
    observer.start( storage.SetHostState )

    connections = ConnectionResource(storage)
    connections_id = ConnectionIdResource(storage)

    api = falcon.API()
    api.add_route('/connections/', connections)
    api.add_route('/connections/{connection_id}', connections_id)
    
    serve(api, host='127.0.0.1', port=5555)

    observer.stop()

if __name__ == "__main__":
    main()