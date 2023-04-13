# ClientVPN / ClientVPN

Showcase a Client VPN with Mutual Authentication

## Building

* Create the Root Certificate that will be signed for all the certificates that the client will present. As per [Create Root CA](https://gist.github.com/fntlnz/cf14feb5a46b2eda428e000157447309). *BEWARE* AWS only accept RSA 1024 or 2048 certificates

```shell
openssl genrsa -out resources/rootCA.key 2048
openssl req -x509 -new -nodes -key resources/rootCA.key -sha256 -days 3650 -subj "/C=ES/ST=MADRID/O=ALLFUNDS S.A.U./OU=ARCHITECTURE LABS/CN=client-vpn-ca.domain.com" -out resources/rootCA.crt
```

* Upload the newly certificate to ACM:

```shell
aws acm import-certificate --certificate fileb://resources/rootCA.crt --private-key fileb://resources/rootCA.key
{
    "CertificateArn": "arn:aws:acm:eu-west-1:123456789012:certificate/ca475787-f5cf-41a4-aac7-8c93f72aaaa2"
}
```

* Set the `CertificateArn` parameter in the `template.yaml` file, and build

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

* Once build you can download the OpenVPN configuration file for the Client VPN:

```shell
aws ec2 export-client-vpn-client-configuration --client-vpn-endpoint-id <ClientVpnEndpoint> --output text | sed -e "s/remote /remote $(whoami)./" > resources/client-config.ovpn
```

* And add the reference to the Client Certificate and Key

```shell
cat >> resources/client-config.ovpn <<EOF
cert rootCA.crt
key rootCA.key
EOF
```

* However that is not all. You might have to replace the 3rd certificate as per [troubleshooting: Certificate error](https://docs.aws.amazon.com/vpn/latest/clientvpn-user/windows-troubleshooting.html#windows-troubleshooting-openvpn-gui)

* You are all set to connect to the Client VPN now. This depends on your OS, but on Ubuntu you can follow [net-vpn-connect](https://help.ubuntu.com/stable/ubuntu-help/net-vpn-connect.html.en)

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ClientVPN
```

## Details

*Author*: rostskadat
