# ElasticBeanstalk / Architecture

Showcase different architecture for Elastic Beanstalk. Namely:
* A Dev environment (EIP + EC2 + RDS master)
* A Prod environment (LB + ASG + EC2 + RDS master)
* A Worker environment

## Building

* You first need to create the `template-app.yaml`  stack in order to create the S3 bucket where you will then upload your application code.

```shell
sam build --template template-app.yaml
sam deploy --guided
``` 

* Then build and zip the Python application, then upload it to the `Bucket`:

```shell
bash flask-hello-world/create_zip_for_eb.sh
aws s3 cp flask-hello-world/build/flask-hello-world.zip <Bucket>
``` 

* Then build the main stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```shell
sam local invoke --event events/events.json ArchitectureFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-Architecture
```

## Details

*Author*: rostskadat
