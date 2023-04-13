# SimpleDesktop

This SAM template is not meant to be used independently but as part of a larger application. Typically you would include the template in your SAM manifest like this:

```yaml
  SimpleDesktop:
    Type: AWS::Serverless::Application
    Properties:
      Location: path/to/SimpleDesktop/template.yaml
      Parameters:
        ParentStackName: 
          Ref: AWS::StackName

...

Outputs:

  SimpleDesktop:
    Description: The SimpleDesktop PublicDnsName
    Value: 
      Fn::GetAtt: SimpleDesktop.Outputs.InstancePublicDnsName

```

It simply create an EC2::Instance from a LaunchTemplate with VNCServer installed...


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


## Connecting with Remmina

First connect to the `InstancePublicDnsName` and start the VNC server 

```shell
ssh -L 5901:localhost:5901 -i <KeyName> ec2-user@<InstancePublicDnsName>
?> ~/start-vnc
```

Then with [Remmina](https://remmina.org/) create a new VNC session with the following characteristics:

On the `Basic` tab:
```
Server: localhost:1
Username: ec2-user
Password: <VncPassword>
```

On the `SSH Tunnel` tab:
```
Custom: <InstancePublicDnsName>
Username: ec2-user
IdentityFile: <KeyName>
```
