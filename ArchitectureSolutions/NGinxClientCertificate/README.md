# ELB / NGinxClientCertificate

Showcase different fault tolerant solutions to allow client authentication through certificate:

* TCP ELB on port 443
* EIP + Route53 + R53 Health check

References:
* [SSL-on-amazon-linux-2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/SSL-on-amazon-linux-2.html)
* [configuring-apache-for-ssl-client-certificate-authentication](https://stuff-things.net/2015/09/28/configuring-apache-for-ssl-client-certificate-authentication/)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You will first need to retrieve the `PKCS12` Client Certificate generated on the instance and install it on your browser (no password required)

```shell
scp <Instance>:/etc/pki/CA/newcerts/client-authentiction.p12 client-authentiction.p12
```

* Then you can simply open the `Instance` using `HTTPS` and present the `client` certificate to see the test page
* After you've done that you can open the `LoadBalancerDNSName` FQDN using `HTTPS` and present the `client` certificate again
* Finally you can open the `RecordSetGroup` FQDN using `HTTPS` and present the `client` certificate again

In all cases you should be able to see the landing page.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-NGinxClientCertificate
```

## Details

*Author*: rostskadat
