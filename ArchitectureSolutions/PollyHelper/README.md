# PollyHelper

# How to build 

```bash
sam build
sam deploy
```

# Adjusting the different url, endpoints, etc...

You need to adjust the following files:

* [static/script.js]: contains the <APIEndpoint> URL

# Deploy the statc content

```bash
aws s3 cp --recursive --acl public-read static/ s3://<WebsiteBucket>/
```

# TODO

Investigate S3 + HTTPS [https://medium.com/@channaly/how-to-host-static-website-with-https-using-amazon-s3-251434490c59]

# Cleaning up

```bash
aws s3 rm --recursive s3://<Mp3Bucket>/
aws s3 rm --recursive s3://<WebsiteBucket>/
aws cloudformation delete-stack --stack-name PollyHelper
```
