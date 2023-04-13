# Lambda / Lambda@Edge

Show case a Lambda@Edge site to transform user request to implement localisation

## Building

Before being able to launch the stack you will need to create the Service role required:

```shell
aws iam create-service-linked-role --aws-service-name replicator.lambda.amazonaws.com
aws iam create-service-linked-role --aws-service-name logger.cloudfront.amazonaws.com
```

Then you can build the stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Once deploy you can load the english page and check that when the `lang=es` query string is added the localised page is returned:

```shell
curl https://<DistributionDomainName>/en/index.html 
<!doctype html><html lang="en"><body>This page is in english</body></html>
curl 'https://<DistributionDomainName>/en/index.html?lang=es' 
<!doctype html><html lang="en"><body>Esta pagina esta en castellano</body></html>
``` 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws --region us-east-1 cloudformation delete-stack --stack-name SAPC01-LambdaAtEdgeWithS3
```

## Details

*Author*: rostskadat
