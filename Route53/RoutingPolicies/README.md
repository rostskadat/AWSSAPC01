# Route53

This stack showcases the different routing policies

## Build the stack

```bash
sam build
# create in Ireland
ln -s samconfig-eu-west-1.toml samconfig.toml
sam deploy 

# create in Sydney
ln -s samconfig-ap-southeast-2.toml samconfig.toml
sam deploy
```

Then create the different Route53 records

```bash
sam build --template template-records.yaml
# create in Ireland
ln -s samconfig-records.toml samconfig.toml
sam deploy 
```

# Testing the records


## Simple record

The response comes alternatively from server 1 in region #1 and from server 2 in region #1

```bash
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-simple.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
...
```

## Weighted record

The response comes alternatively from server 1 in region #1 and from server 2 in region #1, then after 5 minutes it comes alternatively from server 1 in region #2 and from server 2 in region #2

```bash
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-weighted.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-206-122-233.ap-southeast-2.compute.amazonaws.com</h1></body></html>
...
```

## Latency record

The response comes from the server with the lowest latency. Open an SSH session on server in region #1 and on a server region #2

```bash
?> ssh ec2-34-255-208-146.eu-west-1.compute.amazonaws.com
eu-west-1> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-latency.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
...
?> ssh ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com
ap-southeast-2> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-latency.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-54-206-122-233.ap-southeast-2.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com</h1></body></html>
...
```

## Latency record

The response comes from the servers in region #1. Then after stopping the EC2 instances in region #1, the response comes from the servers in region #2

```bash
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-failover.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
...
# Shutdown the instances in region #1 
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-failover.afbaws.com/ ; sleep 1; done
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-206-122-233.ap-southeast-2.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com</h1></body></html>
...
```

## Latency record

The response comes from the servers in region #1. Then after stopping the EC2 instances in region #1, the response comes from the servers in region #2

```bash
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-failover.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
...
# Shutdown the instances in region #1 
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-failover.afbaws.com/ ; sleep 1; done
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-206-122-233.ap-southeast-2.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com</h1></body></html>
...
```

## Geolocation record

The response comes from the servers in region #1 when the . Then after stopping the EC2 instances in region #1, the response comes from the servers in region #2

```bash
?> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-geolocation.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-3-250-20-174.eu-west-1.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-34-255-208-146.eu-west-1.compute.amazonaws.com</h1></body></html>
...
?> ssh ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com
ap-southeast-2> while (true); do curl -s -H 'Cache-Control: no-cache' http://route53-geolocation.afbaws.com/ ; sleep 1; done
...
<html><body><h1>Hello from ec2-54-206-122-233.ap-southeast-2.compute.amazonaws.com</h1></body></html>
<html><body><h1>Hello from ec2-54-66-217-41.ap-southeast-2.compute.amazonaws.com</h1></body></html>
...
```


## Cleanup the stack

```bash
aws cloudformation delete-stack --region eu-west-1 --stack-name Route53Records
aws cloudformation delete-stack --region eu-west-1 --stack-name Route53
aws cloudformation delete-stack --region ap-southeast-2 --stack-name Route53
```
