# CodeDeploy / DeployToEC2

Showcase deploying to EC2 instance (could be on-premise server)

## Building

* Build the resources required by the stack

```shell
sam build --template template-bucket.yaml
sam deploy --guided
``` 

* Build and deploy the main stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

You should be able to navigate to the `index.html` of the newly deployed application

```shell
curl http://<EC2Instance>/
<!doctype html>

<html lang="en-us">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Flask Application</title>
  </head>

  <body>
    <p>Hello World!</p>
  </body>
</html>
```

* You can then create a new application version by updating the `application.tgz` tarball and executing a new deployment (i.e. from the console). You can also check that the `gunicorn` changes on the instance

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DeployToEC2
```

## References:

* [reference-appspec-file-example](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-example.html#appspec-file-example-server)

## Details

*Author*: rostskadat
