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

from prometheus_client.core import REGISTRY
from prometheus_client import start_wsgi_server
from exporter import *


class CeilometerMetrics(object):

    def __init__(self, port_,log_):
        self.logger = log_
        self.collectors = {}
        self.collectors['cpu_util'] = CpuUtilCollector.CpuUtilCollector()
        self.collectors['cpu'] = CpuCollector.CpuCollector()
        self.collectors['cpu.delta'] = CpuDeltaCollector.CpuDeltaCollector()
        self.collectors['disk.read.requests.rate'] = DiskRRCollector.DiskRRCollector()
        self.collectors['disk.write.requests.rate'] = DiskWRCollector.DiskWRCollector()
        self.collectors['network.incoming.bytes.rate'] = NetworkINRCollector.NetworkINRCollector()
        self.collectors['network.incoming.packets.rate'] = NetworkINPRCollector.NetworkINPRCollector()
        self.collectors['network.outgoing.packets.rate'] =NetworkOUTPRCollector.NetworkOUTPRCollector()
        self.collectors['network.outgoing.bytes.rate'] = NetworkOUTRCollector.NetworkOUTRCollector()
        self.collectors['network.incoming.packets'] = NetworkINPCollector.NetworkINPCollector()
        self.collectors['network.outgoing.packets'] = NetworkOUTPCollector.NetworkOUTPCollector()
        self.collectors['network.incoming.bytes'] = NetworkINBCollector.NetworkINBCollector()
        self.collectors['network.outgoing.bytes'] = NetworkOUTBCollector.NetworkOUTBCollector()
        self.collectors['disk.read.bytes.rate'] = DiskRBRCollector.DiskRBRCollector()
        self.collectors['disk.write.bytes.rate'] = DiskWBRCollector.DiskWBRCollector()
        self.collectors['memory.usage'] = MemUsageCollector.MemUsageCollector()


        REGISTRY.register(self.collectors['cpu_util'])
        REGISTRY.register(self.collectors['cpu'])
        REGISTRY.register(self.collectors['cpu.delta'])
        REGISTRY.register(self.collectors['disk.read.requests.rate'])
        REGISTRY.register(self.collectors['disk.write.requests.rate'])
        REGISTRY.register(self.collectors['network.incoming.bytes.rate'])
        REGISTRY.register(self.collectors['network.incoming.packets.rate'])
        REGISTRY.register(self.collectors['network.outgoing.packets.rate'])
        REGISTRY.register(self.collectors['network.outgoing.bytes.rate'])
        REGISTRY.register(self.collectors['network.incoming.packets'])
        REGISTRY.register(self.collectors['network.outgoing.packets'])
        REGISTRY.register(self.collectors['network.incoming.bytes'])
        REGISTRY.register(self.collectors['network.outgoing.bytes'])
        REGISTRY.register(self.collectors['disk.read.bytes.rate'])
        REGISTRY.register(self.collectors['disk.write.bytes.rate'])
        REGISTRY.register(self.collectors['memory.usage'])

        self.run_server(int(port_))

    def update(self,msg_):

        if msg_['counter_name'] in self.collectors.keys():
            #self.logger.info('Mt: '+ msg_['counter_name']+" value: "+str(msg_['counter_volume'])+" timestamp: "+msg_['timestamp'])
            #print('Metric Updated! (%s)' % msg_['counter_name'])
            self.collectors[msg_['counter_name']].update(msg_)
        else:
            self.logger.info('Collector NOT found! (%s %s %s)' % (msg_['counter_name'], msg_["counter_unit"], msg_["counter_type"]))

    def run_server(self, port_):
        print ("READY to START Exporter")
        start_wsgi_server(port_)
        self.logger.info('Exporter started in port: ' + str(port_))
