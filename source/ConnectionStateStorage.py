#!/usr/bin/env python

class ConnectionStateStorage:
    def __init__(self):
        self._states = {} # (ip, port) = state

    def addHost(self, ip, port):
        key = (ip,port)
        self._states[key] = False

    def deleteHost(self, ip, port):
        del self._states[(ip, port)]

    def SetHostState(self, ip, port, state):
        key = (ip,port)
        if not self._states.has_key(key):
            return
        self._states[key] = state

    def GetHostState(self, ip, port):
        key = (ip, port)
        if not key in self._states:
            return (key[0], key[1], False)
        return (key[0], key[1], self._states[key])


class ConnectionStorage:
    def __init__(self):
        self._ids = {} # id = (ip, port)
        self._currentId = 0

    def addHost(self, ip, port):
        key = (ip,port)
        self._currentId += 1
        self._ids[self._currentId] = key
        return self._currentId

    def deleteHost(self, id):
        del self._ids[id]

    def GetHosts(self):
        return self._ids.items()

    def GetHostById(self, id):
        return self._ids.get(id)

    def GetIdByHost(self, ip, port):
        for item in self._ids.items():
            if item[1][0] == ip and item[1][1] == port:
                return item[0]
        return None