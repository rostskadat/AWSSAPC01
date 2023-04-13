# EC2Instance

This SAM template is not meant to be used independently but as part of a larger application. Typically you would include the template in your SAM manifest like this:

```yaml
  FileSystem:
    Type: AWS::Serverless::Application
    Properties:
      Location: path/to/EFS/template.yaml
      Parameters:
        VpcId: 
          Ref: VpcId
        Subnets:
          Ref: Subnets
...

Outputs:

  FileSystem:
    Description: The FileSystem
    Value: 
      Fn::GetAtt: FileSystem.Outputs.FileSystem

```

It simply create an EFS File System

