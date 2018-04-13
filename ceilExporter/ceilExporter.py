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

import logging, os
from logging.handlers import RotatingFileHandler
from udpSrv.thrSrv import ThrSrv
from exporter import CeilometerMetrics
from Configure import Configuration



def init():
    global exporter_port
    global udpSrv_port
    conf = Configuration("exporter.conf")
    exporter_port = os.getenv('CEXP_PORT', conf.ConfigSectionMap("exporter")['port'])
    udpSrv_port = os.getenv('UDPSRV_PORT', conf.ConfigSectionMap("udp_server")['port'])

if __name__ == '__main__':
    logger = logging.getLogger('ceilometerCollector')
    hdlr = RotatingFileHandler('ceilCollector.log', maxBytes=1000000, backupCount=1)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.WARNING)
    logger.setLevel(logging.INFO)
    init()

    logger.info('====================')
    logger.info('Ceilometer Collector')
    logger.info('Exporter port: ' + exporter_port)
    logger.info('UDP server port: ' + udpSrv_port)
    cmMtr = CeilometerMetrics.CeilometerMetrics(exporter_port,logger)
    srv = ThrSrv('0.0.0.0',udpSrv_port,cmMtr,logger)

