# PreSignedURL

Showcase the use of pre-signed URL to download and upload S3 objects 

* More information about the download can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/ShareObjectPreSignedURL.html) 
* More information about the upload can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/PresignedUrlUploadObject.html)

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can upload and download a file using the helpers
```
python3 helpers\s3_download_presigned_url.py --bucket <Bucket> --key s3object --dst-file s3object
python3 helpers\s3_upload_presigned_url.py --bucket <Bucket> --key s3object --src-file s3object
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-PreSignedURL
```
