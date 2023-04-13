# GlobalAccelerator / BlueGreen

Showcase GlobalAccelerator in order to avoid Client DNS caching during Blue Green deployment

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

*NOTE* both `Blue` and `Green` instances are behind the same `EndpointGroup` which means that there are no affinitiy between a client and an specific instance. It means that if the application is statefull, this scenario will not work. In order for the scenario to properly work we should have two `EndpointGroup`, where client affinity can be controlled with the `Listener.ClientAffinity` attribute. The downside of this scenario is that the `EndpointGroup` must be in 2 different regions...

```shell
while (true); do echo $(curl -s <AppUrl>); sleep 1; done
<html><head><title>BLUE</title></head><body style="background-color: cornflowerblue;"><p>This is the BLUE page</p></body></html>
<html><head><title>BLUE</title></head><body style="background-color: green;"><p>This is the GREEN page</p></body></html>
<html><head><title>BLUE</title></head><body style="background-color: cornflowerblue;"><p>This is the BLUE page</p></body></html>
<html><head><title>BLUE</title></head><body style="background-color: cornflowerblue;"><p>This is the BLUE page</p></body></html>
...
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-BlueGreen
```

## Details

*Author*: rostskadat
