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

from prometheus_client.core import GaugeMetricFamily, GaugeMetricFamily, REGISTRY


class CpuUtilCollector(object):
    data = {
        'source': 'openstack',
        'counter_type': 'gauge',
        'project_id': '9f89d937198543e6b38a89d8503142d5',
        'timestamp': '2018-03-21T16:27:45.273549',
        'resource_id': '50a3a175-42a4-42d4-8a10-e0f0cf16c1a0',
        'message_id': 'c97bb281-2d24-11e8-9c8a-150e18cb77dc',
        'user_id': 'cf180fadfb214e12aa90a5ccafe10383',
        'message_signature': 'dd6c21aa535dbc188e9991ea24a889203ca3eb52c5297a04e1bdef09c9905c7b',
        'resource_metadata': {
            'os_type': 'hvm',
            'display_name': 'test',
            'image_ref': '6fadef71-6608-4ba2-9cee-671a1aa5edba',
            'task_state': '',
            'instance_host': 'pike2',
            'root_gb': 1,
            'state': 'running',
            'name': 'instance-00000006',
            'memory_mb': 512,
            'flavor': {
                'swap': 0,
                'disk': 1,
                'ram': 512,
                'vcpus': 1,
                'ephemeral': 0,
                'name': 'm1.tiny',
                'id': '76949218-7a4f-4e7e-8269-f4e24c2832ab'
            },
            'architecture': 'x86_64',
            'vcpus': 1,
            'instance_id': '50a3a175-42a4-42d4-8a10-e0f0cf16c1a0',
            'disk_gb': 1,
            'instance_type': 'm1.tiny',
            'ephemeral_gb': 0,
            'status': 'active',
            'image_ref_url': None,
            'cpu_number': 1,
            'image': {
                'id': '6fadef71-6608-4ba2-9cee-671a1aa5edba'
            },
            'host': '30b3a202bf71d8651cf49f4aa9232f79e029f87d47c081163fca9d12'
        },
        'counter_name': 'cpu_util',
        'counter_unit': '%',
        'monotonic_time': None,
        'counter_volume': 2.0722654293387963
    }

    val1 = 0
    val2 = 0
    metric_name = 'cpu_util'
    metrics = []

    def collect(self):
        # yield GaugeMetricFamily('my_gauge', 'Help text', value=7)
        if len(self.metrics) > 0:
            self.c = GaugeMetricFamily(self.metric_name.replace(".","_"), 'CPU utilization percentage',
                                       labels=['resource_id', 'project_id', 'user_id','counter_unit', 'display_name'])
            for mt in self.metrics:
                self.c.add_metric([mt['resource_id'], mt['project_id'], mt['user_id'], mt['counter_unit'], mt['resource_metadata']['display_name']],
                                  mt['counter_volume'])
            yield self.c

    def update(self, msg):
        if msg['counter_name'] == self.metric_name:
            for (i,mt) in enumerate(self.metrics):
                if mt['resource_id'] == msg['resource_id']:
                    self.metrics[i]['counter_volume'] = msg['counter_volume']
                    return
            self.metrics.append(msg)