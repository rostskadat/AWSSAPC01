# ElasticBeanstalk / WebServerAndWorker

Showcase a Web Server and Worker decoupling architecture.
It is an implementation of slide *352*

## Building

*BEWARE* This uses the [EB Cli](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html) (instead of the usual [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html))

* Develop your applications (or skip to the deployment part)

```shell
cd WebServerAndWorker
virtualenv virt
source virt/bin/activate
pip install -r requirements.txt
```

* Initialize the Elastic Beanstalk environment and accept the default

```shell
eb init WebServerAndWorker \
    --region eu-west-1 \
    --keyname SAPC01 \
    --modules WebServer Worker \
    --platform python-3.7 \
    --tags PLATFORM=SAPC01
```

* Then create the environments 

```shell
eb create --modules WebServer Worker --env-group-suffix dev
...
```

* Finally iteratively deploy your current code in your environments

```shell
eb deploy --modules WebServer Worker --env-group-suffix dev --staged
...
```

* Look at the logs of your environment:

```shell
cd WebServer
eb ssh 
...
sudo tail -F /var/log/web.stdout.log
```



* [create-deploy-python-flask](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
* [using-features.migration-al](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.migration-al.html#using-features.migration-al.specific)

## Testing

You can trigger the download of a specific ZTF Daily Alert tarball by posting to the `/download` URL

```shell
cd WebServer
eb status | grep CNAME
  CNAME: WebServer-dev.eba-mzndk9ap.eu-west-1.elasticbeanstalk.com
curl -X POST http://<CNAME>/download?date=20200913
...
```



## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
eb terminate WebServerAndWorker-dev
```

## Details

*Author*: rostskadat
