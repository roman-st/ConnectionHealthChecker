#!/usr/bin/env python
import falcon
import json

class ConnectionIdResource():
    def __init__(self, storage):
        self._storage = storage

    def on_get(self, req, resp, connection_id):
        id = int(connection_id)
        if not self._storage.FindHost(id):
            resp.status = falcon.HTTP_404
        else:
            state = self._storage.GetHostState(id)
            obj = {'id' : id, 'ip' : state[0], 'port' : state[1], 'state': state[2]}
            resp.body = json.dumps(obj)

class ConnectionResource():
    def __init__(self, storage):
        self._storage = storage

    def on_get(self, req, resp):
        hosts = []
        for item in self._storage.GetHosts():
            obj = {'id' : item[0], 'ip' : item[1][0], 'port' : item[1][1]}
            hosts.append(obj)
        
        resp.body = json.dumps(hosts)