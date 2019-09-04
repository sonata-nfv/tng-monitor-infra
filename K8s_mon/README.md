# Kubernetes cluster monitoring 
<p align="justify">5GTANGO/SONATA monitoring system is able to collect information from kubernetes clusters based on the Prometheus server. This functionality requires the deployment of a Prometheus instance inside the k8s cluster and the configuration of the 5GTANGO/SONATA monitoring system to collect Prometheus.      

The required monitoring pods inside the kubernetes cluster are:
 * Grafana
 * Prometheus 
 * Pushgateway 
 * Alertmanager (optional)

### Dependencies
 * python 2.7
 
### Development
To contribute to the development of the monitoring probes you have to fork the repository, commit new code and create pull requests.


### Installation
a. Deployment
```
kubectl apply -f /home/tango/k8s-monitoring.yaml
```

b. Get pods
```
kubectl get pods -n sonata

NAME                                          READY   STATUS    RESTARTS   AGE
grafana-core-7b84f8fb56-x9rhh                 1/1     Running   0          12s
son-alertmanager-deployment-98c6c4548-6bfhm   1/1     Running   0          12s
son-prometheus-deployment-8558fc9444-bmfl9    1/1     Running   0          12s
son-pushgateway-deployment-794cd78755-qx7nl   1/1     Running   0          12s

```

c. Configure monitoring sytem to collect data from the kubernetes cluster 
```
kubectl get pods -n sonata

NAME                                          READY   STATUS    RESTARTS   AGE
grafana-core-7b84f8fb56-x9rhh                 1/1     Running   0          12s
son-alertmanager-deployment-98c6c4548-6bfhm   1/1     Running   0          12s
son-prometheus-deployment-8558fc9444-bmfl9    1/1     Running   0          12s
son-pushgateway-deployment-794cd78755-qx7nl   1/1     Running   0          12s

```

## License

This SDN monitoring probe is published under Apache 2.0 license. Please see the LICENSE file for more details.

### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Karkazis  (pkarkazis)
 * Panos Trakadas  (trakadasp)

### Feedback-Chanel

* Please use the GitHub issues to report bugs.