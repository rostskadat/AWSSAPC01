# OpsWorksHelloWorld

Simple Hello World OpsWorks stack

## Building

* Build the resources required by the stack

```shell
sam build --template template-bucket.yaml
sam deploy --guided
``` 

## Create the Chef Cookbook

* Reference [opsworks-linux-demo-cookbook-nodejs](https://github.com/aws-samples/opsworks-linux-demo-cookbook-nodejs)

## Create the NodeJs Application

* Reference [build-a-simple-app-using-node-js-and-mysql](https://dev.to/achowba/build-a-simple-app-using-node-js-and-mysql-19me)

Modify `npm install step`:

```shell
npm install express express-fileupload body-parser mysql ejs req-flash aws-sdk --save
```

* Upload the cookbook and check that it is accessible:

```shell
tar cvzf cookbook.tgz cookbook 
aws s3 cp cookbook.tgz s3://<Bucket>/

curl <CustomCookbooksUrl> --output cookbook.tgz
```

* Build and deploy the main OpsWorks stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Troubleshooting

### Your cookbook fails

* Log into the failed instance

* Update the cookbook

```shell
sudo opsworks-agent-cli run_command update_custom_cookbooks
sudo opsworks-agent-cli run_command deploy
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-OpsWorksHelloWorld
```

## References

* [gettingstarted-cookbooks](https://docs.aws.amazon.com/opsworks/latest/userguide/gettingstarted-cookbooks.html)

## Details

*Author*: rostskadat
