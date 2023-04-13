# IAMAuthentication

This sample showcases the use of IAM authentication and Admin password rotation for an MySQL DB.
It will configure the DB to use IAM user, and periodically rotate the DBAdmin password.
This is an implementation of the tutorial [tutorials_db-rotate](https://docs.aws.amazon.com/secretsmanager/latest/userguide/tutorials_db-rotate.html) and [users-connect-rds-iam](https://aws.amazon.com/premiumsupport/knowledge-center/users-connect-rds-iam/)

Finally it demonstrate an EC2 instance that uses a role in order to access the DBInstance, and thus allows to not store *any* password on the machine.

One of the first thing that the EC2Instance does is to connect to the DB and run the initialization script as per the tutorial

## References

* The IAM Role for the EC2Instance is described [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.IAMPolicy.html)
* For SSL connection refer to this [page](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html#MySQL.Concepts.SSLSupport)

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You can connect by connecting to the EC2Instance, and execute the following shell command

```shell
MASTER_PASSWORD=$(aws --region eu-west-1 secretsmanager get-secret-value --secret-id "$SECRET_ID" --query 'SecretString' --output text | jq -r '.password')
mysql --host=db-sapc01-iamauthentication.cgbdhswg43m4.eu-west-1.rds.amazonaws.com --port=3306 --user=administrator --password=$MASTER_PASSWORD
Welcome to the MariaDB monitor.  Commands end with ; or \g.
...
```

You can then force the secret rotation:

```shell
aws --region eu-west-1 secretsmanager rotate --secret-id "$SECRET_ID" --query 'SecretString' --output text | jq -r '.password')
```

After it has completed you should be able to connect with the new password.

```shell
MASTER_PASSWORD=$(aws --region eu-west-1 secretsmanager get-secret-value --secret-id "$SECRET_ID" --query 'SecretString' --output text | jq -r '.password')
mysql --host=db-sapc01-iamauthentication.cgbdhswg43m4.eu-west-1.rds.amazonaws.com --port=3306 --user=administrator --password=$MASTER_PASSWORD
Welcome to the MariaDB monitor.  Commands end with ; or \g.
...
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name SAPC01-IAMAuthentication
```
