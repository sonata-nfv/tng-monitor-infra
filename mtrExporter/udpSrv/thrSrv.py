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
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class Echo(DatagramProtocol):
    def __init__(self, ceilColl_, log_):
        self.logger = log_
        self.collector = ceilColl_


    def datagramReceived(self, data, addr):
        global pks
        pks += 1
        try:
            msg = msgpack.loads(data, encoding="utf-8")
            #print('pks '+str(pks))
            #print(msg['resource_id'], msg['counter_name'], msg['counter_type'], msg['counter_unit'],msg['counter_volume'], msg['timestamp'])
            self.transport.write(msgpack.dumps(''), addr)
            if self.collector:
                self.collector.update(msg)
        except msgpack.exceptions.BufferFull:
            print('msgpack.exception BufferFull ')
            pass
        except msgpack.exceptions.ExtraData:
            print('msgpack.exception ExtraData ')
            pass
        except msgpack.exceptions.OutOfData:
            print('msgpack.exception OutOfData ')
            pass
        except msgpack.exceptions.PackException:
            print('msgpack.exceptionPackException ')
            pass
        except msgpack.exceptions.PackOverflowError:
            print('msgpack.exception PackOverflowError ')
            pass
        except msgpack.exceptions.PackValueError:
            print('msgpack.exception PackValueError ')
            pass
        except msgpack.exceptions.UnpackException:
            print('msgpack.exception UnpackException ')
            pass
        except msgpack.exceptions.UnpackValueError:
            print('msgpack.exception UnpackValueError ')
            pass

class ThrSrv(object):

    def __init__(self, ip_, port_,ceilColl_, log_):
        self.logger = log_
        self.collector = ceilColl_
        HOST, PORT = ip_, int(port_)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)
        server = (HOST, PORT)
        sock.bind(server)
        global pks
        pks = 0
        print("Listening on " + HOST + ":" + str(PORT))
        count = 0
        port = reactor.adoptDatagramPort(
            sock.fileno(), socket.AF_INET, Echo(ceilColl_=self.collector,log_=self.logger))
        sock.close()
        reactor.run()

if __name__ == "__main__":

    ThrSrv("0.0.0.0", 10000)

