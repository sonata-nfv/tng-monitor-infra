# Libvirt Exporter



```

                      +---------------+               +----------------+
                      |    libvirt    |      http     |                |
                      |    Exporter   <---------------+   Prometheus   +
                      |               |               |                |
                      +---------------+               +----------------+
                                     
```

### Dependencies
 * python3
 * libvirt-python
 * prometheus-client
 

### Installation

Build container
```
docker build -t son-monitor-libvirtexp .
```

Run monitoring probe as container
```
docker run --privileged -d -p 9093:9091 -v /var/run/libvirt/libvirt-sock:/var/run/libvirt/libvirt-sock --name son-monitor-virtExporter son-monitor-libvirtexp
```

### Development

To contribute to the development of the 5GTango ceilometer exporter you have to fork the repository, commit new code and create pull requests.


### License

Metrics Exporter is published under Apache 2.0 license. Please see the LICENSE file for more details.

### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Karkazis  (pkarkazis)
 * Panos Trakadas  (trakadasp)

### Feedback-Chanel
* Please use the GitHub issues to report bugs.

