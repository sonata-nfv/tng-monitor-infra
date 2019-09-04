# Kubernetes cluster monitoring 
<p align="justify">5GTANGO/SONATA monitoring system is able to collect information from kubernetes clusters based on the Prometheus server. This functionality requires the deployment of a Prometheus instance inside the k8s cluster and the configuration of the 5GTANGO/SONATA monitoring system to collect Prometheus.      

### Installing / Getting started
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

c. Get services
```
kubectl get services -n sonata

NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
grafana                    NodePort    10.99.64.99     <none>        3000:30000/TCP                  14d
kube-state-metrics         ClusterIP   10.99.85.236    <none>        8080/TCP                        14d
pushgateway                NodePort    10.108.157.32   <none>        9091:30091/TCP                  14d
son-alertmanager-service   NodePort    10.100.174.81   <none>        9093:30093/TCP                  14d
son-prometheus-service     NodePort    10.101.241.54   <none>        9090:30090/TCP,9089:30089/TCP   14d

```

c. Configure monitoring system to collect data from the kubernetes cluster 
```
curl -X POST "http://<monitoring_manager_ip>:8000/api/v2/prometheus/targets" -H "accept: application/json" -H "Content-Type: application/json"  -d "{ \"targets\": [ { \"honor_labels\": true, \"job_name\": \"K8s_cluster\", \"metrics_path\": \"/federate\", \"params\": { \"match[]\": [ \"{job=\\\"kubernetes-cadvisor\\\"}\", \"{job=\\\"kubernetes-nodes\\\"}\", \"{job=\\\"kubernetes-pods\\\"}\", \"{job=\\\"pushgateway\\\"}\" ] }, \"scrape_interval\": \"10s\", \"scrape_timeout\": \"10s\", \"static_configs\": [ { \"targets\": [ \"<k8s-cluster-ip>:30090\" ] } ] }, { \"job_name\": \"prometheus\", \"static_configs\": [ { \"targets\": [ \"localhost:9090\" ] } ] }, { \"job_name\": \"pushgateway\", \"static_configs\": [ { \"targets\": [ \"localhost:9090\" ] } ] } ]}"

```

## Developing

The required monitoring pods inside the kubernetes cluster are:
 * Grafana
 * Prometheus 
 * Pushgateway 
 * Alertmanager (optional)
 
 
### Submiting changes
To contribute to the development of the monitoring probes you have to fork the repository, commit new code and create pull requests.


## Licensing

This SDN monitoring probe is published under Apache 2.0 license. Please see the LICENSE file for more details.

## Versioning
The most up-to-date version is v5.0.

### Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

 * Panos Karkazis  (pkarkazis)
 * Panos Trakadas  (trakadasp)

### Feedback-Chanel

* You may use the mailing list [sonata-dev-list](mailto:sonata-dev@lists.atosresearch.eu)
* You may use the GitH