# DatabaseMigrationService / MySQL2PostgreSQL

Showcase migration from MySQL to PostgreSQL. It uses an existing DB, and therefore the Subnet must be chosen with care such that the ReplicationInstance and TragetDB are in the same VPC as the Source DB...

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json MySQL2PostgreSQLFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-MySQL2PostgreSQL
```

## Details

*Author*: rostskadat
