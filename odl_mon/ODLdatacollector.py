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

import json,urllib2, base64
import datetime,time,logging,os
import time,datetime
from configure import configuration
from servers import server
from DtFiltering import valdt 

controller_ip = "192.168.1.231"


def init():
    global prometh_server
    global odl_server
    global node_name
    global user
    global logger
        
    #read configuration
    conf = configuration("odc.conf")
    #odl_server = conf.ConfigSectionMap("ODL_server")['odl_url']
    #prometh_server = conf.ConfigSectionMap("Prometheus")['server_url']
    #node_name = conf.ConfigSectionMap("ODL_server")['node_name']
    #user = json.loads(conf.ConfigSectionMap("ODL_server")['user'])

    odl_server = os.getenv('ODL_SRV', conf.ConfigSectionMap("vm_node")['odl_url'])
    prometh_server = os.getenv('PROM_SRV', conf.ConfigSectionMap("Prometheus")['server_url'])
    node_name =  os.getenv('NODE_NAME', conf.ConfigSectionMap("Prometheus")['node_name']) 
    user =  os.getenv('USR_CRED', conf.ConfigSectionMap("Prometheus")['user'])

    logger = logging.getLogger('dataCollector')
    hdlr = logging.FileHandler('dataCollector.log', mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    #logger.error('We have a problem')
    logger.info('OpenDayLight Data Collector')
    logger.info('ODL Server '+odl_server)
    logger.info('Promth Server '+prometh_server)
    logger.info('Monitoring Node '+node_name)
          
            
def getNodes(creds):
    try: 
        url = odl_server+"/restconf/operational/opendaylight-inventory:nodes"
        req = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (creds[0]['user_name'], creds[0]['password'])).replace('\n', '')
        
        req.add_header("Authorization", "Basic %s" % base64string) 
        req.add_header('Content-Type','application/json')

        response=urllib2.urlopen(req)
        code = response.code
        logger.info('Response code from ODL: '+str(code))
        data = json.loads(response.read())
        return data
        
    except urllib2.HTTPError, e:

        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:

        logger.warning('Error: '+str(e))
    except ValueError, e:

        logger.warning('Error: '+str(e))
        

        
def postNode(node):
    nodeId = "id=\""+node['id']+"\", serial_number=\""+node['flow-node-inventory:serial-number']+"\", hardware=\""+node['flow-node-inventory:hardware']+"\", manufacturer=\""+node['flow-node-inventory:manufacturer']+"\", software=\""+node['flow-node-inventory:software']+"\""
    timestamp = " "+str(int(datetime.datetime.now().strftime("%s")) * 1000)
    #ports
    port_state_live="# TYPE port_state_live gauge" + '\n'
    port_state_blocked="# TYPE port_state_blocked gauge" + '\n'
    port_state_link_down="# TYPE port_state_link_down gauge" + '\n'
    port_maximum_speed="# TYPE port_maximum_speed gauge" + '\n'
    port_current_speed="# TYPE port_current_speed gauge" + '\n'
    port_receive_frame_error="# TYPE port_receive_frame_error gauge" + '\n'
    port_packets_transmitted="# TYPE port_packets_transmitted gauge" + '\n'
    port_packets_received="# TYPE port_packets_received gauge" + '\n'
    port_collision_count="# TYPE port_collision_count gauge" + '\n'
    port_receive_over_run_error="# TYPE port_receive_over_run_error gauge" + '\n'
    port_receive_crc_error="# TYPE port_receive_crc_error gauge" + '\n'
    port_transmit_errors="# TYPE port_transmit_errors gauge" + '\n'
    port_receive_drops="# TYPE port_receive_drops gauge" + '\n'
    port_transmit_drops="# TYPE port_transmit_drops gauge" + '\n'
    port_receive_errors="# TYPE port_receive_errors gauge" + '\n'
    
    for port in node['node-connector']:
        portId = ",port=\""+port['flow-node-inventory:port-number']+"\", mac=\""+port['flow-node-inventory:hardware-address']+"\""
        
        port_state_live+="port_state_live{"+nodeId+portId+"}"+str(boolean2int(port['flow-node-inventory:state']['live'])) + timestamp + '\n'
        port_state_blocked+="port_state_blocked{"+nodeId+portId+"}"+str(boolean2int(port['flow-node-inventory:state']['blocked'])) + timestamp + '\n'
        port_state_link_down+="port_state_link_down{"+nodeId+portId+"}"+str(boolean2int(port['flow-node-inventory:state']['link-down'])) + timestamp + '\n'
        port_maximum_speed+="port_maximum_speed{"+nodeId+portId+"}"+str(port['flow-node-inventory:maximum-speed']) + timestamp + '\n'
        port_current_speed+="port_current_speed{"+nodeId+portId+"}"+str(port['flow-node-inventory:current-speed']) + timestamp + '\n'
        port_receive_frame_error+="port_receive_frame_error{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-frame-error']) + timestamp + '\n'
        port_packets_transmitted+="port_packets_transmitted{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['transmitted']) + timestamp + '\n'
        port_packets_received+="port_packets_received{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']['received']) + timestamp + '\n'
        port_collision_count+="port_collision_count{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['collision-count']) + timestamp + '\n'
        port_receive_over_run_error+="port_receive_over_run_error{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-over-run-error']) + timestamp + '\n'
        port_receive_crc_error+="port_receive_crc_error{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-crc-error']) + timestamp + '\n'
        port_transmit_errors+="port_transmit_errors{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['transmit-errors']) + timestamp + '\n'
        port_receive_drops+="port_receive_drops{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-drops']) + timestamp + '\n'
        port_transmit_drops+="port_transmit_drops{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['transmit-drops']) + timestamp + '\n'
        port_receive_errors+="port_receive_errors{"+nodeId+portId+"}"+str(port['opendaylight-port-statistics:flow-capable-node-connector-statistics']['receive-errors']) + timestamp + '\n'
        
    data = port_state_live+port_state_blocked+port_state_link_down+port_maximum_speed+port_current_speed+port_receive_frame_error+port_packets_transmitted+port_packets_received+port_collision_count+port_receive_over_run_error+port_receive_crc_error+port_transmit_errors+port_receive_drops+port_transmit_drops+port_receive_errors
    #print data
    url = prometh_server+"/job/ports/instance/"+node_name
    logger.info('Post on: \n'+url)
    logger.info('Post ports metrics: \n'+data)
    try: 
        req = urllib2.Request(url)
        req.add_header('Content-Type','text/html')
        req.get_method = lambda: 'PUT'
        response=urllib2.urlopen(req,data)
        code = response.code
        
        logger.info('Response Code: '+str(code))      
    except urllib2.HTTPError, e:
        logger.warning('Error: '+str(e))
    except urllib2.URLError, e:
        logger.warning('Error: '+str(e))




def boolean2int(bool):
    if bool:
        return 1
    return 0

def date2int(str_date):
    date = datetime.datetime.strptime(str_date,"%Y-%m-%dT%H:%M:%SZ")
    return  time.mktime(date.timetuple())

def getStates(vms):
    states ={}
    for vm in vms:
        if vm['status'] in states:
            states[vm['status']] += 1
        else:
            states[vm['status']] = 1
    return states
    
if __name__ == "__main__":
    #print "OpenDayLight Data Collector"
    init()
    
    
    nodes = getNodes(user)
    for node in nodes['nodes']['node']:
        postNode(node)

