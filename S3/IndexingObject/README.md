# IndexingObject

Showcase how to index objects upon storing them into S3. *Beware* The `IndexingObjectFunction` function only index text files.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

Upload different object into S3 and then query words information from DynamoDB.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-IndexingObject
```
