# Download Daily Alert

A simple application that download the daily tar from https://ztf.uw.edu/alerts/public/ and uncompress it into an S3 bucket

## Running the example

You might need to mount your aws credentials in order to run the docker command

```shell
docker build -t download-daily-alerts .
docker run -v ~/.aws:/root/.aws -v /tmp:/tmp download-daily-alerts --date 20200913 --outptu-dir /tmp
```

This would result in the file [ztf_public_20200913.tar.gz](https://ztf.uw.edu/alerts/public/ztf_public_20200913.tar.gz) being downloaded and expanded into `s3://mybucket/alerts/2020/09/12`.
