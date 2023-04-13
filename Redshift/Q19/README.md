# Q19

## Question

```
Amazon's Redshift uses which block size for its columnar storage

A. 2KB

B. 8KB

C. 16KB

D. 32KB

E. 1024KB
```

## Answer

`E`

```bash
sam build
sam deploy
ssh <Instance>
Instance> sudo yum install python3 python3-devel postgresql-devel gcc -y
Instance> sudo python3 -m pip install psycopg2
Instance> ./healthcheck.py
Using psycopg2...
DUAL=1

```

## Cleanup

```bash
aws cloudformation delete-stack --stack-name RedshiftQ19
```
