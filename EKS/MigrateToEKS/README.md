# EKS / MigrateToEKS

Showcase the use of EKS and related services

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

### Configure kubectl

Once the `Cluster` is up and running you must configure your `kubectl` command to access it as per [create-kubeconfig](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)

```shell
aws eks update-kubeconfig --name <Cluster> 
...
kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   73m
``` 

### Deploy the sample application

Once `kubectl` is configured, you can deploy the sample application:

```shell
kubectl apply -f manifest/service/access/hello-world.yaml
namespace/sample created
deployment.apps/hello-world created
service/hello-world-service created
``` 

## Service 

Then expose the service

```shell
#?> kubectl expose deployment -n sample hello-world --type=NodePort --name=example-service
#service/example-service exposed
?> kubectl describe services -n sample
Name:              hello-world-service
Namespace:         sample
Labels:            <none>
Annotations:       Selector:  name=hello-world
Type:              ClusterIP
IP:                10.100.96.156
Port:              <unset>  80/TCP
TargetPort:        8080/TCP
Endpoints:         <none>
Session Affinity:  None
Events:            <none>

```

*NOTE* take note of the `NodePort`

Then get your deployment:

```shell
?> kubectl get pods -n sample --selector="run=load-balancer-example" --output=wide
NAME                          READY   STATUS    RESTARTS   AGE     IP              NODE                                                  NOMINATED NODE   READINESS GATES
hello-world-b746b89bd-kk72g   1/1     Running   0          6m20s   172.31.51.125   fargate-ip-172-31-51-125.eu-west-1.compute.internal   <none>           <none>
hello-world-b746b89bd-lnjr8   1/1     Running   0          8m49s   172.31.65.49    fargate-ip-172-31-65-49.eu-west-1.compute.internal    <none>           <none>

```

*NOTE* take note of the `IP`


Then log into the `EC2Instance` (since the pods are spun in a private subnet) and use curl to get the URL:

```shell
# curl http://<public-node-ip>:<NodePort>
curl http://172.31.51.125:31287

```



## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-MigrateToEKS
```

## Details

*Author*: rostskadat
