# ElastiCache / RedisSession

Showacse the use of Redis RBAC, AOF, for Session Managment.

Is creates an NodeJS apps supported by an RDS database and a Redis Cache Cluster. The wole stack is deployed in ElasticBeanstalk (as is is the most straight forward)...

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Start the application locally

```shell
LOG4JS_LEVEL=debug PORT=3000 REGION=eu-west-1 SECRET_ARN=${Secret} REDIS_HOST=${ReplicationGroupEndpointAddress} RDS_HOST=${DBInstanceEndpointAddress} \
    nodemon .
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-RedisSession
```

## Details

*Author*: rostskadat
