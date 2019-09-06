[![Build Status](http://jenkins.sonata-nfv.eu/buildStatus/icon?job=tng-monitor-infra/master)](http://jenkins.sonata-nfv.eu/job/tng-monitor-infra/master) [![Gitter](https://badges.gitter.im/sonata-nfv/Lobby.svg)](https://gitter.im/sonata-nfv/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
<p align="center"><img src="https://github.com/sonata-nfv/son-monitor/wiki/images/sonata-5gtango-logo-500px.png" /></p>


# Infrastructure monitoring
<p align="justify">5GTANGO/SONATA monitoring framework collects data from NFVI, VNFs hosted on VMs or containers, VIMs and ODL servers. The implemented framework provides the following tools for collecting data from NFVIs and SDN switches. 

 * Metric exporter provides an alternative way to gather monitoring data for VMs using Ceilometer (OpenStack).
 * Libvirt exporter gathers monitoring data for VMs accessing directly the libvirt hyperviror
 * Kubernetes configuration for the collecting monitoring metrics for containers deployed in kubernetes cluster
 * ODL exporter collects data from SDN controllers 

## Installing / Getting started
See more information in each component's reademe file

## Developing
To contribute to the development you have to fork the repository, commit new code and create pull requests.

## Licensing
Infrastructure monitoring probes are published under Apache 2.0 license. Please see the LICENSE file for more details.


#### Lead Developers
The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Karkazis  (pkarkazis)
 * Panos Trakadas  (trakadasp)

####  Feedback-Channel

- You may use the mailing list [sonata-dev-list](mailto:sonata-dev@lists.atosresearch.eu)
- Gitter room [![Gitter](https://badges.gitter.im/sonata-nfv/Lobby.svg)](https://gitter.im/sonata-nfv/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
