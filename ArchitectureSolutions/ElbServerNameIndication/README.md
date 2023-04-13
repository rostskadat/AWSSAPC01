# ELB / ElbServerNameIndication

Showcase the Use of SNI for an ELB. With just one ALB you can upload several Certificate in order to serves several Sites on the same ELB and allow the client to use different FQDN, and receive the proper certificate

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can simply check that each subdomain is request is directed to the proper instance:


```shell
> curl -k https://default.domain.com
default
> curl -k https://subdomain1.domain.com
subdomain1
> curl -k https://subdomain2.domain.com
subdomain2
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ElbServerNameIndication
```

## Details

*Author*: rostskadat
