#!/usr/bin/env python
import falcon
import json

class ConnectionIdResource():
    def __init__(self, healthChecker):
        self._healthChecker = healthChecker

    def on_get(self, req, resp, connection_id):
        id = int(connection_id)
        if not self._healthChecker.FindHostById(id):
            resp.status = falcon.HTTP_404
        else:
            state = self._healthChecker.GetHostState(id)
            obj = {'id' : id, 'ip' : state[0], 'port' : state[1], 'state': state[2]}
            resp.body = json.dumps(obj)

class ConnectionResource():
    def __init__(self, healthChecker):
        self._healthChecker = healthChecker
        
    def on_get(self, req, resp):
        hosts = []
        for item in self._healthChecker.GetHosts():
            obj = {'id' : item[0], 'ip' : item[1][0], 'port' : item[1][1]}
            hosts.append(obj)
        resp.body = json.dumps(hosts)

    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        ip, port = data['ip'], data['port']

        if self._healthChecker.FindHost(ip, port):
            resp.status = falcon.HTTP_400
            return
        self._healthChecker.addHost(ip, port)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        id = data['id']

        if not self._healthChecker.FindHostById(id):
            resp.status = falcon.HTTP_400
            return
        self._healthChecker.deleteHost(id)
        resp.status = falcon.HTTP_200
