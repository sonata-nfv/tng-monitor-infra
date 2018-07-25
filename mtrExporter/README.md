# Metrics Exporter

5GTANGO/SONATA metrics exporter uses the pipeline mechanism provided by [openstack ceilometer](https://docs.openstack.org/ceilometer/latest/admin/telemetry-data-pipelines.html) in order to collect monitoring data for all the VMs inside openstack NFVI and expose them to the [Prometheus.io](https://github.com/prometheus) server. The main advantage of this approach is that all VNFs that are hosted in VMs can be monitored without the need of any additional software or configuration. The supported monitoring metrics are defined in ceilometer side:

```

      +----------------+                +---------------+               +----------------+
      |                |       udp      |               |      http     |                |
      +  ceilometer    +---------------->  mtrExporter  <---------------+   Prometheus   +
      |                |                |               |               |                |
      +----------------+                +---------------+               +----------------+
                                     
```

### Dependencies
 * python
 * configparser
 * msgpack
 * prometheus-client
 * setuptools
 

### Installation

Build container
```
docker build -t son-monitor-ceilexp
```

Run monitoring probe as container
```
docker run -d --name son-monitor-ceilExporter -p 10000:10000/udp -p 9092:9091 son-monitor-ceilexp
```

### Development

To contribute to the development of the 5GTango ceilometer exporter you have to fork the repository, commit new code and create pull requests.


### License

Metrics Exporter is published under Apache 2.0 license. Please see the LICENSE file for more details.

### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Trakadas  (trakadasp)
 * Panos Karkazis  (pkarkazis)

### Feedback-Chanel
* Please use the GitHub issues to report bugs.

