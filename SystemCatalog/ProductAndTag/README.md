# SystemCatalog / ProductAndTag

Showcase the use of the SystemCatalog service

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

After building the stack you can launch the product by:

```shell
aws servicecatalog create-provisioned-product-plan
   --plan-name <value>
   --plan-type <value>
   [--notification-arns <value>]
   [--path-id <value>]
   --product-id <Product>
   --provisioned-product-name EC2FlaskInstance-03151831
   --provisioning-artifact-id <value>
   [--provisioning-parameters <value>]
   [--idempotency-token <value>]
   [--tags <value>]
   [--cli-input-json <value>]
   [--generate-cli-skeleton <value>]
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-ProductAndTag
```

## Details

*Author*: rostskadat
