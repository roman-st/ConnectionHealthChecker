#!/usr/bin/env python

import argparse
import falcon
from ConnectionObserver import ConnectionObserver
from ResourceHandlers import ConnectionResource, ConnectionIdResource
from ConnectionStateStorage import ConnectionStateStorage
from waitress import serve

def get_hosts(args):
    hosts = args.strip().split(",")
    hosts = map(lambda s: s.split(":"), hosts)
    hosts = map(lambda x: (x[0], int(x[1])), hosts)
    return hosts

def get_args():
    parser = argparse.ArgumentParser(description='Service for check connection availability')
    parser.add_argument('-c', '--connection', type=str, help='Connection endpoint list', required=True)
    return parser.parse_args().connection

def main():
    hosts = get_hosts(get_args())

    storage = ConnectionStateStorage(hosts)

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