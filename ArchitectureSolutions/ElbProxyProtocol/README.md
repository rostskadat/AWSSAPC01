# ELB / ElbProxyProtocol

Showcase the use of the Proxy Protocol in an ELB. It allows the backend to knonw the IP of the client even when using the a TCP ELB

Reference: 
* [using-proxy-protocol](https://docs.nginx.com/nginx/admin-guide/load-balancer/using-proxy-protocol/)
* [targetgroupattribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticloadbalancingv2-targetgroup-targetgroupattribute.html)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can simply use the `curl` to retrieve the index page on port `80`. 
*NOTE*: You can not query the `Instance` directly since it expect the Proxy Protocol connection header first.
When you query the `LoadBalancerDNSName` you can see the `X-Real-Ip` header filled with the value of the Client IP

```shell
> curl http://<LoadBalancerDNSName>/
{"created_at": "2021-01-21'T'10:38:14", "headers": [{"Host": "sapc0-loadb-1bft3aqgpho4c-b4a6901a74668bc1.elb.eu-west-1.amazonaws.com"}, {"X-Real-Ip": "129.35.108.66"}, {"Connection": "close"}, {"Content-Length": "0"}, {"User-Agent": "curl/7.50.3"}, {"Accept": "*/*"}, {"Cache-Control": "max-stale=0"}, {"X-Bluecoat-Via": "dcf701849d46d6c4"}]}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ElbProxyProtocol
```

## Details

*Author*: rostskadat
