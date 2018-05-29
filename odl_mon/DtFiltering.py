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

import os, subprocess
from time import sleep
import sys,time,datetime,json

class valdt:
    
    def __init__(self):
        self.prev_dt = None
        self.curr_dt = None
        
        

    def validateDT(self,enable_, dt_):
        metric_hdr = ''
        dt2go = ''
        
        if not enable_:
            return dt_
        
        if self.prev_dt is None:
            self.prev_dt = self.str2obj(dt_)
            return dt_
        else:
            flag = False
            for line in dt_.splitlines():
                if line.startswith('#'):
                    metric_hdr = line
                    flag = False
                else:
                    c_name = self.getMetricName(line, 'name')
                    c_val = self.getMetricName(line, 'value')
                    c_updated = self.getMetricName(line, 'time')
                    if c_name not in self.prev_dt:
                        if not flag:
                            dt2go += metric_hdr + '\n'
                            flag = True
                        dt2go += line+ '\n'
                        self.prev_dt[c_name]={}
                        self.prev_dt[c_name]['value'] = c_val
                        self.prev_dt[c_name]['last_update'] = c_updated
                        continue
                    if self.chDetla(c_name, c_val, c_updated):
                        if not flag:
                            dt2go += metric_hdr  + '\n'
                            flag = True
                        dt2go += line + '\n'
                        continue
                    if self.chTime(c_name, c_val, c_updated):
                        if not flag:
                            dt2go += metric_hdr +'\n'
                            flag = True
                        dt2go += line + '\n'
                        continue
            return dt2go
                    
                
                    
    def chDetla(self, c_name_, c_val_, c_updated_):
        #print ""+self.prev_dt[c_name_]['value']+" "+c_val_
        if c_name_ in self.prev_dt:
            if float(self.prev_dt[c_name_]['value']) == 0 and float(c_val_) == 0:
                return False
            if float(self.prev_dt[c_name_]['value']) == 0:
                denom = c_val_
            else:
                denom = self.prev_dt[c_name_]['value']
             
            if (abs(float(self.prev_dt[c_name_]['value']) - float(c_val_))/float(denom) > 0.1):
                self.prev_dt[c_name_]['value'] = c_val_
                self.prev_dt[c_name_]['last_update'] = c_updated_
                return True
        return False
        
    def chTime(self,c_name_, c_val_, c_updated_):
        if c_name_ in self.prev_dt:
            if int(c_updated_) - int(self.prev_dt[c_name_]['last_update']) > 5*60*1000:
                self.prev_dt[c_name_]['value'] = c_val_
                self.prev_dt[c_name_]['last_update'] = c_updated_
                return True
            else:
                return False
    
    
    def str2obj(self, data_):
        dt = {}
        for line in data_.splitlines():
            if line.startswith('#'):
                continue
            self.metric_obj(line,dt)
        return dt
            

    def metric_obj(self, ln_,dt_):
        name = self.getMetricName(ln_, 'name')
        val = self.getMetricName(ln_, 'value')
        updated = self.getMetricName(ln_, 'time')
        dt_[name]={}
        dt_[name]['value'] = val
        dt_[name]['last_update'] = updated
        return 
    
    def getMetricName(self,ln_, key_):
        ptr = ln_.find('}',0)
        if key_ == 'name':
            return ln_[0:ptr+1]
        if key_ == 'value':
            return ln_[ptr+1:ln_.find(' ',ptr)].strip()
        if key_ == 'time':
            return ln_[ln_.find(' ',ptr+1):len(ln_)].strip()
        else:
            return None
    

