# DMS / SchemaConversionTool

Showcase the use of the SCT to convert MySQL Schema to Postgres. It will connect to an existing MySQL DB, extract the schema and then create it back into the Postgres DB

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 
Look at [ec2-linux-2-install-gui/](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-2-install-gui/) for how to connect to your instance

## Testing

You can connect to the `InstancePublicDnsName` and start the VNC server:

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

Then connect and open the menu `Applications >> Other >> AWS Schema Conversion Tool` and follow the instructions to connect to the DataBase, save the Assesement Report , etc.

*NOTE* make sure that the DB SecurityGroup allow connection from your Instance. 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-SchemaConversionTool
```

## Details

*Author*: rostskadat
