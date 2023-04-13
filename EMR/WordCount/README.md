# EMR / WordCount

Showcase a sample EMR Cluster

## Building

* First build the stack

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

* Once the `Bucket` has been created you can then upload the `WordCount.jar` to the S3 `Bucket`

```shell
aws s3 cp WordCount.jar s3://Bucket/bin/WordCount.jar 
``` 

* Then add the step again to run it (once the jar is available).

```shell
aws emr add-steps --cluster-id <Cluster> \
    --steps Name=CountWordCli,ActionOnFailure=CONTINUE,Jar=s3://<Bucket>/bin/WordCount.jar,Args=WordCount,s3://<Bucket>/input,s3://<Bucket>/output
``` 

## Testing

The hard way:

* Connect to the EMR `MasterPublicDNS`

```shell
ssh ec2-user@<MasterPublicDNS>
?> export JAVA_HOME=/usr/lib/jvm/java-1.8.0-amazon-corretto.x86_64
?> export PATH=${JAVA_HOME}/bin:${PATH}
?> export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
?> ...
?> # copy and paste the Java class and then compile
?> hadoop com.sun.tools.javac.Main WordCount.java
?> jar cf wc.jar WordCount*.class
?> hadoop jar wc.jar WordCount s3://<Bucket>/input s3://<Bucket>/output
?> aws s3 cp s3://<Bucket>/output/part-r-00000 .
?> head part-r-00000
Aenean  2
Aliquam 3
Cras    3
...
?>
``` 

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-WordCount
```

## Reference:

* [MapReduceTutorial](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Example:_WordCount_v1.0)

## Details

*Author*: rostskadat
