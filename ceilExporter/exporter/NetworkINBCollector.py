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


class NetworkINBCollector(object):

    metric_name = 'network.incoming.bytes'
    metrics = []

    def collect(self):
        if len(self.metrics) > 0:
            self.c = CounterMetricFamily(self.metric_name.replace(".","_"), 'Network incoming bytes counter',
                                       labels=['resource_id', 'project_id', 'user_id','counter_unit','vnic_name','mac', 'display_name'])
            for mt in self.metrics:
                self.c.add_metric([mt['resource_id'], mt['project_id'], mt['user_id'], mt['counter_unit'], mt['resource_metadata']['vnic_name'],
                                   mt['resource_metadata']['mac'], mt['resource_metadata']['display_name']], mt['counter_volume'])
            yield self.c

    def update(self, msg):
        if msg['counter_name'] == self.metric_name:
            #print(msg)
            for (i,mt) in enumerate(self.metrics):
                if mt['resource_id'] == msg['resource_id']:
                    self.metrics[i]['counter_volume'] = msg['counter_volume']
                    return
            self.metrics.append(msg)