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

from prometheus_client.core import CounterMetricFamily
import time

class NetworkOUTPCollector(object):

    metric_name = 'network.outgoing.packets'
    metrics = {}

    def collect(self):
        if len(self.metrics) > 0:
            self.c = CounterMetricFamily(self.metric_name.replace(".","_"), 'Network outgoing packets counter',
                                       labels=['resource_id', 'project_id', 'user_id','counter_unit','vnic_name','mac', 'display_name'])
            
            for mt in self.metrics.copy():
              ts = time.time()
              if self.metrics_obj[mt]['last_pushed'] + 4 * self.metrics_obj[mt]['epoch'] > ts:
                self.c.add_metric([self.metrics[mt]['resource_id'],
                                   self.metrics[mt]['project_id'],
                                   self.metrics[mt]['user_id'],
                                   self.metrics[mt]['counter_unit'],
                                   self.metrics[mt]['resource_metadata']['vnic_name'],
                                   self.metrics[mt]['resource_metadata']['mac'],
                                   self.metrics[mt]['resource_metadata']['display_name']],
                                  self.metrics[mt]['counter_volume'])
              else:
                self.metrics_obj.pop(mt)
                continue
            yield self.c

    def update(self, msg):
        ts = time.time()
        if msg['counter_name'] == self.metric_name:
            if not msg['resource_id'] in self.metrics_obj:
                msg['epoch'] = ts
                msg['last_pushed'] = ts
            else:
                msg['epoch'] = ts - self.metrics_obj[msg['resource_id']]['last_pushed']
                msg['last_pushed'] = ts
            self.metrics_obj[msg['resource_id']] = msg