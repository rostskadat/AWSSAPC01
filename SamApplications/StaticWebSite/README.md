# StaticWebSite

This SAM template is not meant to be used independently but as part of a larger application. Typically you would include the template in your SAM manifest like this:

```yaml
  StaticWebSite:
    Type: AWS::Serverless::Application
    Properties:
      Location: path/to/StaticWebSite/template.yaml
```

*BEWARE* : it uses the Cloudformation [S3Objects](https://github.com/awslabs/aws-cloudformation-templates/tree/master/aws/services/CloudFormation/MacrosExamples/S3Objects) Macro.