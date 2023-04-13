# S3WebsiteConfiguration

## Build the stack 

```bash
?> sam build
?> sam deploy
```

# Test the stack

Open the `BucketWebsiteURL` in a browser. If access denied, make index.html public.

## Delete the stack

```bash
?> aws s3 rm --recursive s3://s3websiteconfiguration-sourcebucket-14nkku6lbsxfr
?> aws cloudformation delete-stack --stack-name S3WebsiteConfiguration
```


