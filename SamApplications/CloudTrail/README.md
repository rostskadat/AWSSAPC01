# CloudTrail

This SAM template is not meant to be used independently but as part of a larger application. Typically you would include the template in your SAM manifest like this:

```yaml
  CloudTrail:
    Type: AWS::Serverless::Application
    Properties:
      Location: path/to/CloudTrail/template.yaml
      Parameters:
        DataEventS3BucketArns:
          # NOTE: the final "/"
          Fn::Sub: "${Bucket1.Arn}/,${Bucket2.Arn}/"
```

It create and configure a CloudTrail object as well as a Athena DB with named queries to access the logs