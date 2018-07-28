## Copyright (c) 2015 SONATA-NFV, 2017 5GTANGO [, ANY ADDITIONAL AFFILIATION]
## ALL RIGHTS RESERVED.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## Neither the name of the SONATA-NFV, 5GTANGO [, ANY ADDITIONAL AFFILIATION]
## nor the names of its contributors may be used to endorse or promote
## products derived from this software without specific prior written
## permission.
##
## This work has been performed in the framework of the SONATA project,
## funded by the European Commission under Grant number 671517 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the SONATA
## partner consortium (www.sonata-nfv.eu).
##
## This work has been performed in the framework of the 5GTANGO project,
## funded by the European Commission under Grant number 761493 through
## the Horizon 2020 and 5G-PPP programmes. The authors would like to
## acknowledge the contributions of their colleagues of the 5GTANGO
## partner consortium (www.5gtango.eu).
# encoding: utf-8

#!/usr/bin/python
import socket
import socketserver, threading, msgpack
from threading import Thread
from socketserver import ThreadingMixIn


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    collector = None

    def handle(self):
        data = self.request[0].strip()
        ### get port number
        port = self.client_address[1]
        ### get the communicate socket
        socket = self.request[1]
        ### get client host ip address
        client_address = (self.client_address[0])
        ### proof of multithread
        cur_thread = threading.current_thread()
        #print ("thread %s" % cur_thread.name)
        #print ("received call from client:%s %s" % (client_address, port))
        if self.collector:
            #print("Collector Exists")
            msg = msgpack.loads(data, encoding="utf-8")
            #print(msg['resource_id'], msg['counter_name'], msg['counter_type'], msg['counter_unit'],msg['counter_volume'], msg['timestamp'])
            # print ("received data: %s" % data)
            self.collector.update(msg)
            #print("--------------")
        else:
            self.logger.info("Collector Doesn't Exist")



class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class ThrSrv(object):

    def __init__(self, ip_, port_,ceilColl_, log_):
        self.logger = log_
        HOST, PORT = ip_, int(port_)
        class ThreadedUDPRequestHandlerCeil(ThreadedUDPRequestHandler):
            collector = ceilColl_
            logger = self.logger

        server = ThreadedUDPServer((HOST, PORT),
                                   ThreadedUDPRequestHandlerCeil)
        ip, port = server.server_address
        server.serve_forever()
        # Start a thread with the server --
        # that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        self.logger.info('UDP server started in port: ' + str(port_))
        server.shutdown()

if __name__ == "__main__":

    ThrSrv("0.0.0.0", 10000)

