# EC2Instance

This SAM template is not meant to be used independently but as part of a larger application. Typically you would include the template in your SAM manifest like this:

```yaml
  EC2Instance:
    Type: AWS::Serverless::Application
    Properties:
      Location: path/to/EC2Instance/template.yaml
      Parameters:
        ParentStackName: 
          Ref: AWS::StackName

...

Outputs:

  EC2Instance:
    Description: The EC2Instance PublicDnsName
    Value: 
      Fn::GetAtt: EC2Instance.Outputs.InstancePublicDnsName

```

It simply create an EC2::Instance from a LaunchTemplate...


## SSM Parameter for latest AMI

You can get the latest AMI for your region by issuing the following command:

* Latest Linux AMI: You can get the latest AMI Linux for your region by issuing the following command

```shell
aws ssm get-parameters-by-path --path /aws/service/ami-amazon-linux-latest --query "Parameters[? Name == '/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2' ].Value" --output text
ami-0bb3fad3c0286ebd5
```

or alternatively use the following parameter in your stack:

```yaml
  ImageId:
    Description: "The Image Id (AMI) to use"
    Type: "AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>"
    Default: "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2"
```

* Latest Windows AMI: You can get the latest AMI Windows for your region by issuing the following command

```shell
aws ssm get-parameters-by-path --path /aws/service/ami-windows-latest --query "Parameters[? Name == '/aws/service/ami-windows-latest/Windows_Server-2019-English-STIG-Core' ].Value" --output text
ami-0b65c1813d92cc713
```

or alternatively use the following parameter in your stack:

```yaml
  ImageId:
    Description: "The Image Id (AMI) to use"
    Type: "AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>"
    Default: "/aws/service/ami-windows-latest/Windows_Server-2019-English-STIG-Core"
```

* ECS optimized command

```shell
aws ssm get-parameters-by-path --path /aws/service/ecs/optimized-ami/amazon-linux-2/recommended --query "Parameters[? Name == '/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id' ].Value" --output text
ami-02e8b3843287bc013
```

or alternatively use the following parameter in your stack:

```yaml
  ImageId:
    Description: "The Image Id (AMI) to use"
    Type: "AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>"
    Default: "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
```

# Caveats:

## AWS::CloudFormation::Init

When creating a `AWS::Serverless::Application` the resource created in CloudFormation (of type `AWS::CloudFormation::Stack`) does not seem to hold any metadata. Therefore a call to DescribeStackResource will not yield any metadata and thus preventing a cross-stack initialization scenariosuch as:

```yaml
  EC2Instance:
    Type: AWS::Serverless::Application
    Metadata:
      AWS::CloudFormation::Init:
        configSets:
          default: [ Install ]
        Install:
          files:
            /root/startup.sh:
              content: |
                #!/bin/bash
                echo "Starting up $(uname -n)"
              mode: "000700"
              owner: root
              group: root
          commands:
            01_startup:
              command: "bash /root/startup.sh"
    Properties:
      Location: path/to/EC2Instance/template.yaml
```

This is further demonstrated by a call to `cfn-get-metadata` within the newly created instance such as: 

```shell
/opt/aws/bin/cfn-get-metadata --verbose --region <Region> --stack <ParentStackName> --resource EC2Instance --role <Role>
Error: EC2Instance does not specify any metadata
```

Thus this stack is only usefull to create a barebone instance with *really* simple `Userdata` property (and no call to `cfn-xxx` tools).

## Instance Store

This stack only create Instance Store Volume for the `m3.medium` instance.
