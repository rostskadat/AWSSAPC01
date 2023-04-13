# AthenaQuickSight / AthenaQuickSight

Demonstrate the use of Athena and QuickSight. Provides an implementation of Slide 329

## Building

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
```

You then have to run the queries we just created:

```shell
aws athena batch-get-named-query --named-query-ids "$(aws athena list-named-queries | jq '.NamedQueryIds')"
...
```

## Testing

* You must download some sample data:

```shell
odate=20200913
remote_file=https://ztf.uw.edu/alerts/public/ztf_public_${odate}.tar.gz
local_file=/tmp/ztf_public_${odate}.tar.gz
local_dir=${local_file%%.tar.gz}
curl ${remote_file} --output ${local_file}
mkdir ${local_dir}
tar xvzf ${local_file} --directory ${local_dir} --overwrite
aws s3 sync ${local_dir} s3://<Bucket>/avro_files/${odate:0:4}/${odate:4:2}/${odate:6:2}

aws athena start-query-execution --query-string "SELECT objectid, candid FROM ztfalertsdb.ztfalerts limit 10;" --result-configuration OutputLocation=s3://<Bucket>/output
```

* Then you can query the data directly from Anthena console

## extracting basic info about candidates

```pyhton
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import SkyCoord

t = Time(2459105.9968519, format='jd')
t.format = 'isot'
print (t.value)
2020-09-13T11:53:25.999
c = SkyCoord(ra=86.832571*u.degree,dec=-18.1636697*u.degree)
print (c)
<SkyCoord (ICRS): (ra, dec) in deg
    (86.832571, -18.1636697)>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-AthenaQuickSight
```

## Reference 

* The schema was extracted using the notebook [Working_with_avro_files.ipynb](../../ECS/BatchProcessing/notebooks/Working_with_avro_files.ipynb)
* [Fritz's User Guide](https://fritz-marshal.org/doc/user_guide.html)

## Details

*Author*: rostskadat
