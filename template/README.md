# SAM Template

This folder contains a basic SAM template that aliviate most common task when creating a new Scenario.
The general form is as follow:

```bash
sam init --no-interactive \
    --runtime python3.8 \
    --dependency-manager pip \
    --location /path/to/AWSSAPC01/template/basic \
    --output-dir /path/to/AWSSAPC01/<Service> \
    --name Scenario 
```

For instance 

```bash
sam init --no-interactive --runtime python3.8 --dependency-manager pip --location template/basic --output-dir CloudWatch --name BillingAlarm 
```
