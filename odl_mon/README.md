# SDN swich monitoring 
<p align="justify">5GTANGO/SONATA ODL (OpenDayLight) monitoring client is used in order to monitor SDN controllers by collecting information from ODL servers and push them to monitoring server. 
The url of the pushgateway monitoring server must be set in node.conf file 

Supported monitoring metrics are:
 * port_state_live
 * port_state_blocked
 * port_state_link_down
 * port_maximum_speed
 * port_current_speed
 * port_receive_frame_error
 * port_packets_transmitted
 * port_packets_received
 * port_collision_count
 * port_receive_over_run_error
 * port_receive_crc_error
 * port_transmit_errors
 * port_receive_drops
 * port_transmit_drops
 * port_receive_errors


### Dependencies
 * python 2.7
 
### Development
To contribute to the development of the monitoring probes you have to fork the repository, commit new code and create pull requests.


### Installation
a. From code
```
export ODL_SRV=http://<odl_server>:<port>
export USR_CRED=[{"user_name": <user_name>, "password":<password>}]
export NODE_NAME=<server_name>
export PROM_SRV=http://<prom_server>:<port>/metrics
sudo python ODLdatacollector.py
```

b. Using container
```
sudo docker build -t son-odl-probe .
sudo docker run -d --name tng-odl-probe -e NODE_NAME=VNF_1 -e ODL_SRV=http://<odl_server>:<port> -e PROM_SRV=http://<pushgateway>:<port>/metrics -e ODL_USER=[{"user_name": <user_name>, "password":<password>}] -e export ODL_PASS=<password> tng-odl-probe
```


## License

This SDN monitoring probe is published under Apache 2.0 license. Please see the LICENSE file for more details.

###Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas  (trakadasp)
 * Panos Karkazis  (pkarkazis)

### Feedback-Chanel

* You may use the mailing list sonata-dev@lists.atosresearch.eu
* Please use the GitHub issues to report bugs.