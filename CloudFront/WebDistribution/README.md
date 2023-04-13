# CloudFrontWebDistribution 

## Build stack

*BEWARE*: you need the [S3Objects](https://github.com/aws-cloudformation/aws-cloudformation-macros) Cloudformation Macro in your account

```bash
?> sam build
?> sam deploy
```

Do not forget to make the S3Object (index.html) public

## Testing

* Create a new instance in Sydney

And test the latency by using the output 

```bash
?> cat > curl-format.txt <<EOF
    time_namelookup:  %{time_namelookup}s\n
       time_connect:  %{time_connect}s\n
    time_appconnect:  %{time_appconnect}s\n
   time_pretransfer:  %{time_pretransfer}s\n
      time_redirect:  %{time_redirect}s\n
 time_starttransfer:  %{time_starttransfer}s\n
                    ----------\n
         time_total:  %{time_total}s\n
EOF
?> curl -w "@curl-format.txt" -o /dev/null -s "https://cloudfrontwebdistribution-sourcebucket-i5qugr0loye0.s3.eu-west-1.amazonaws.com/index.html"
    time_namelookup:  0.005352s
       time_connect:  0.260123s
    time_appconnect:  0.786039s
   time_pretransfer:  0.786084s
      time_redirect:  0.000000s
 time_starttransfer:  1.053691s
                    ----------
         time_total:  1.053783s
?> curl -w "@curl-format.txt" -o /dev/null -s "https://d3tj5g5n40kh8j.cloudfront.net/index.html"
    time_namelookup:  0.023491s
       time_connect:  0.024750s
    time_appconnect:  0.037287s
   time_pretransfer:  0.037318s
      time_redirect:  0.000000s
 time_starttransfer:  1.107549s
                    ----------
         time_total:  1.107607s
?> curl -w "@curl-format.txt" -o /dev/null -s "https://d3tj5g5n40kh8j.cloudfront.net/index.html"
    time_namelookup:  0.004186s
       time_connect:  0.005389s
    time_appconnect:  0.017374s
   time_pretransfer:  0.017407s
      time_redirect:  0.000000s
 time_starttransfer:  0.024003s
                    ----------
         time_total:  0.024055s
```

*NOTE*: how the first get from CloudFront is slow while the second one is fast...


## Delete

```bash
?> aws cloudformation delete-stack --stack-name CloudFrontWebDistribution
```
