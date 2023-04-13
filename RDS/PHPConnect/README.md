# SAAC02RDS


This stack ilustrate the RDS Lab

## Build the stack

```bash
sam build
sam deploy 
```

## Open the instance

```bash
?> curl -s http://ec2-63-33-208-150.eu-west-1.compute.amazonaws.com/connect.php

```


## Cleanup the stack

```bash
aws cloudformation delete-stack --stack-name SAAC02RDS
```
