# CloudFront / DynamicStatic

Showcase Dynamic / Static Content separation and corresponding caching strategies

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

* First check that the `StaticOrigin` is up and running:

```shell
while true; do echo $(curl -s <StaticOrigin>) ; sleep 1 ; done
{"created_at": "2020-11-09'T'11:54:08"}
{"created_at": "2020-11-09'T'11:54:09"}
...
```

* Once done, point to the `StaticDistribution` to warm up the cache and make sure that the `created_at` does not change.

```shell
while true; do echo $(curl -s <StaticDistribution>) ; sleep 1 ; done
{"created_at": "2020-11-09'T'11:14:08"}
{"created_at": "2020-11-09'T'11:14:08"}
...
```

Do the same for the `DynamicOrigin` and `DynamicDistribution` :

```shell
while true; do echo $(curl -s <DynamicOrigin>) ; sleep 1 ; done
{"created_at": "2020-11-09'T'11:55:02"}
{"created_at": "2020-11-09'T'11:55:03"}
...
while true; do echo $(curl -s <DynamicDistribution>) ; sleep 1 ; done
{"created_at": "2020-11-09'T'11:34:43"}
{"created_at": "2020-11-09'T'11:34:43"}
...
```

*Note* how the `DynamicDistribution` respond when we pass the special `sapc01-cache-key` header:

```shell
while true; do echo $(curl -s -H 'sapc01-cache-key: 1' <DynamicDistribution>) ; sleep 1 ; done
{"created_at": "2020-11-09'T'11:55:43"}
{"created_at": "2020-11-09'T'11:55:43"}
...
while true; do echo $(curl -s -H "sapc01-cache-key: $(date)" <DynamicDistribution>) ; sleep 1 ; done
{"created_at": "2020-11-09'T'11:56:21"}
{"created_at": "2020-11-09'T'11:56:22"}
...
```



## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-DynamicStatic
```

## Details

*Author*: rostskadat
