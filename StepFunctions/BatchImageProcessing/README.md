# StepFunctions / BatchImageProcessing

Showcase a 2 level Image processing pipeline.

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

* Copy the images resources from the `images` folder into the `Bucket`

```shell
aws s3 sync images s3://<Bucket>
```

* Start the execution of the `ProcessAllImagesStateMachine`

```shell
aws stepfunctions start-execution --state-machine-arn <ProcessAllImagesStateMachine> | jq -r .executionArn
```

* Wait for it to finish

```shell
aws stepfunctions describe-execution --execution-arn <executionArn>
{
    "executionArn": "arn:aws:states:eu-west-1:123456789012:execution:ProcessAllImagesStateMachine-zWCcEAQKxWvm:c1be32f9-8883-4c91-ac0b-103a07ab318e",
    "stateMachineArn": "arn:aws:states:eu-west-1:123456789012:stateMachine:ProcessAllImagesStateMachine-zWCcEAQKxWvm",
    "name": "c1be32f9-8883-4c91-ac0b-103a07ab318e",
    "status": "SUCCEEDED",
    "startDate": 1616508997.958,
    "stopDate": 1616509013.667,
...
```

* Look at the thumbnails in `ThumbnailBucket`

```shell
aws s3 ls s3://<ThumbnailBucket>
2021-03-23 15:16:43       5534 img_0001.jpg
2021-03-23 15:16:45       2012 img_0002.jpg
2021-03-23 15:16:47       4584 img_0003.jpg
2021-03-23 15:16:49       3457 img_1771.jpg
2021-03-23 15:16:51       5047 img_2158.jpg
```

* And the content of the `ImageMetadata`

```shell
aws dynamodb scan --table-name <ImageMetadata> | jq .Items[0].exif_data.M.DateTime
{
  "S": "2003:12:14 12:01:44"
}
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-BatchImageProcessing
```

## Details

*Author*: rostskadat
