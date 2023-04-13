# KinesisVideoStream / FaceRekognition

Showcase a sample Kinesis Video Stream consumer to rekognize face in a video stream

References:
* [tutorial](https://aws.amazon.com/blogs/machine-learning/easily-perform-facial-analysis-on-live-feeds-by-creating-a-serverless-video-analytics-environment-with-amazon-rekognition-video-and-amazon-kinesis-video-streams/)

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You will need an image of yourself and upload it to the bucket...

```shell
aws s3 cp resources/YourFace.jpg s3://<Bucket>
```

And then index the face:

```shell
aws rekognition index-faces --image '{"S3Object":{"Bucket":"<Bucket>","Name":"YourFace.jpg"}}' --collection-id <RekognitionCollection> --detection-attributes "ALL" --external-image-id "YourName"
{
    "FaceRecords": [
        {
            "Face": {
                "FaceId": "9e7c6953-d3d1-43cf-96bd-0608d0e52309",
                "BoundingBox": {
                    "Width": 0.42237067222595215,
...
```

```shell
sam local invoke --event events/events.json FaceRekognitionFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-FaceRekognition
```

## Details

*Author*: rostskadat
