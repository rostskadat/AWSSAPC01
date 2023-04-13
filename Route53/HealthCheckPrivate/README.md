# HealthCheckPrivate

Showcase how to have a Route53 Health Check based on the health of a private resource.
Basically we have a default RecordSet configured to monitor a CW Alarm.
When the alarm is in the state `ALARM` the RecordSet redirect to an S3 buket with webconfiguration enabled. 
The CW Alarm simulate the fact that some resources are not accessible within a VPC (private subnet).

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You test the `Route53` healthcheck by putting a CloudWatch Metric (and thus raising) an alarm. You do that from the command line.

```shell
while true; do aws cloudwatch put-metric-data --namespace SAPC01-HealthCheckPrivate --metric-name Failover --value 1 ; echo -n . ; sleep 30 ; done
```

If you wait for a minute or more the Alarm will go back to being in `OK` state

while the Alarm is in the `ALARM` state, you can check that the `Route53` record does not return the normal page, but the failover webpage

```shell
while true ; do echo -n "$(date '+%H:%M:%S'): " ; curl https://<WebSite> ; sleep 10 ; done
{"message":"Hello World from Flask!"}
...

```



## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-HealthCheckPrivate
```
