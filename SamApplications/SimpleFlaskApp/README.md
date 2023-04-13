# EC2Instance

This SAM template is not meant to be used independently but as part of a larger application. Typically you would include the template in your SAM manifest like this:

```yaml
  SimpleFlaskApp:
    Type: AWS::Serverless::Application
    Properties:
      Location: path/to/SimpleFlaskApp/template.yaml
      Parameters:
        ParentStackName: 
          Ref: AWS::StackName

...

Outputs:

  SimpleFlaskApp:
    Description: The SimpleFlaskApp PublicDnsName
    Value: 
      Fn::GetAtt: SimpleFlaskApp.Outputs.InstancePublicDnsName

```

It simply create an EC2::Instance from a LaunchTemplate with Flask installed...

