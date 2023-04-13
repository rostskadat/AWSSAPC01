# CloudFront / Origins

Show case the different CloudFront Origins

*References* :
* [DownloadDistValuesDomainName](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-web-values-specify.html#DownloadDistValuesDomainName)


## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can test each Distribution (you will notice the Redirect to HTTPS):

```shell
curl -L http://<S3DistributionDomainName>
...
curl -L http://<S3WebsiteDistributionDomainName>
...
curl -L http://<EC2InstanceDistributionDomainName>
...
```

For the `Failover` distribution you need to shutdown the EC2Main instance in order to simulate the failover capability:

```shell
curl -L http://<FailoverDistribution>
...
EC2MainInstance
...
ssh <EC2MainInstancePublicDnsName>
?> vi /flask-hello-world/app.py # change "return_code = 500"
?> ps -aufx | grep gunicorn
?> kill -HUP gunicorn_pid # reload gunicorn
curl -L http://<FailoverDistribution>
...
EC2FailoverInstance
...
ssh <EC2MainInstancePublicDnsName>
?> vi /flask-hello-world/app.py # change "return_code = 200"
?> ps -aufx | grep gunicorn
?> kill -HUP gunicorn_pid # reload gunicorn
curl -L http://<FailoverDistribution>
...
EC2MainInstance
...
```




## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Origins
```

## Details

*Author*: rostskadat
