# ElasticTranscoder

[CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) does not provide a way to create [ElasticTranscoder](https://docs.aws.amazon.com/elastictranscoder/latest/developerguide/introduction.html) Pipelines. This [Custom Resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) allows you to create such a Pipeline from within your Cloudformation template.

## Create the ElasticTranscoderPipeline Custom Resource

You first need to create the ElasticTranscoderPipeline Custom Resource by executing the stack:

```bash
cd resources/ElasticTranscoderPipeline
sam build
sam deploy
cd ../..
```

## Using the ElasticTranscoderPipeline

You can then reference the ElasticTranscoderPipeline in your CloudFormation template.

```bash
sam build
sam deploy
```

That will create an ElasticTranscoder Pipeline that you can then use to convert videos by simply uploading your files to the S3 <InputBucket>. Once converted your video will be available in the S3 <OutputBucket>

```bash
aws s3 cp /path/to/video.mp4 s3://<InputBucket>
aws --profile <User> s3 cp /path/to/video.mp4 s3://<InputBucket>
aws s3 cp s3://<OutputBucket> /path/to/converted_video.mp4


aws --profile batch-elastictranscoder-eu-west-1 s3 cp /home/rostskadat/Documents/2020.05.14.Titulo\ Preliminar.mp4 s3://elastictranscoder-inputbucket-175d1dy9r9312
```

*BEWARE*: The example stack uses the [SamPolicyTemplateTranslator](https://github.com/awslabs/aws-cloudformation-templates) and the [Yaml2Json](https://github.com/awslabs/aws-cloudformation-templates) CloudFormation Macros. You will need to have created them in your accoutn before hand

## Cleaning up

```bash
aws cloudformation delete-stack --stack-name ElasticTranscoder
```
