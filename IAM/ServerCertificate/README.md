# IAM / ServerCertificate

Showcase a Server Certificate in IAM instead of ACM

## Building

No stack is required

## Testing

First generate a certificate

```shell
FQDN=$(hostname -f)
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout PrivateKey.pem -out Certificate.pem -subj "/C=ES/ST=MADRID/L=MADRID/O=EXAMPLE/CN=${FQDN}"
# Test it...
openssl x509 -in Certificate.pem -text -noout
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            7c:29:f9:9b:ea:d9:71:00:ec:32:e8:ca:d0:06:9b:20:d4:1a:3f:67
...
```

And then upload it to `IAM`:

```shell
aws iam upload-server-certificate --server-certificate-name ${FQDN}
                                    --certificate-body file://Certificate.pem
                                    --private-key file://PrivateKey.pem
{
    "ServerCertificateMetadata": {
        "Path": "/",
        "ServerCertificateName": "sorgenfri",
        "ServerCertificateId": "ASCA3QU7W3EAQAKDBJN72",
        "Arn": "arn:aws:iam::123456789012:server-certificate/sorgenfri",
        "UploadDate": "2021-01-31T15:33:22Z",
        "Expiration": "2031-01-29T15:32:23Z"
    }
}
aws iam get-server-certificate --server-certificate-name ${FQDN}
{
    "ServerCertificate": {
        "ServerCertificateMetadata": {
            "Path": "/",
            "ServerCertificateName": "sorgenfri",
            "ServerCertificateId": "ASCA3QU7W3EAQAKDBJN72",
...
aws iam delete-server-certificate --server-certificate-name ${FQDN}
...
aws iam list-server-certificates
{
    "ServerCertificateMetadataList": []
}
```

## Details

*Author*: rostskadat
