# Libvirt Exporter

Libvirt exporter gathers monitoring data for VMs accessing directly the libvirt hyperviror

```

                      +---------------+               +----------------+
                      |    libvirt    |      http     |                |
                      |    Exporter   <---------------+   Prometheus   +
                      |               |               |                |
                      +---------------+               +----------------+
                                     
```

### Installing / Getting started

Build container
```
docker build -t son-monitor-libvirtexp .
```

Run monitoring probe as container
```
docker run --privileged -d -p 9093:9091 -v /var/run/libvirt/libvirt-sock:/var/run/libvirt/libvirt-sock --name son-monitor-virtExporter son-monitor-libvirtexp
```

## Developing

### Built With

 * python3
 * libvirt-python
 * prometheus-client
 

### Submiting changes

To contribute to the development of the 5GTango/SONATA monitoring framwork you have to fork the repository, commit new code and create pull requests.

## Versioning

The most up-to-date version is v5.0.

### Licensing

Metrics Exporter is published under Apache 2.0 license. Please see the LICENSE file for more details.

### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Karkazis  (pkarkazis)
 * Panos Trakadas  (trakadasp)

### Feedback-Chanel

* You may use the mailing list [sonata-dev-list](mailto:sonata-dev@lists.atosresearch.eu)
* You may use the GitHub issues to report bugs

