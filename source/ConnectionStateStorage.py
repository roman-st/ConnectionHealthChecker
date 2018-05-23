#!/usr/bin/env python

class ConnectionStateStorage:
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