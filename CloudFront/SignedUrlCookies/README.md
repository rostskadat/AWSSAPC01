# CloudFront / SignedUrlCookies

Showcase the use of Signed URL & Cookies.

* Signed URLs are mainly used to protect individual files or for HTTP client that do not support Cookie.
* Signed Cookies are used to protect a whole swath of the distribution

It showcase this in the following scenario:

- Let the user view a public page
- Protect an "installation file" that only paid customer can download
- Protect "subscriber file" in a reserved area of the website

## Building

You can either use the already generated keys or create one of your own:

* Create an SSH Key:

```shell
ssh-keygen -b 2048 -t rsa -C "SAPC01-DEFAULT-KEY" -f keys/SAPC01-DEFAULT-KEY
```

* Then you can export the Public par in the `PEM` format:

```shell
ssh-keygen -e -m pem -f keys/SAPC01-DEFAULT-KEY
-----BEGIN RSA PUBLIC KEY-----
...
```

Copy and paste this into the stack for `Parameters.EncodedKey.Default` and then build the stack:

```shell
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing open the application

Open the `ApplicationUrl` to test the different scenarios

## Testing Public file

* Download the public `index.html`. No key required:

```shell
curl https://<Distribution>/index.html
<!doctype html><html lang="en"><body>This page is public</body></html>
```

## Testing Signed URL

* Try to download the `signed_urls/index.html` protected by Signed URLs and it will fail

```shell
curl https://<Distribution>/signed_urls/index.html
<?xml version="1.0" encoding="UTF-8"?><Error><Code>MissingKey</Code><Message>Missing Key-Pair-Id query parameter or cookie value</Message></Error>
```

### Testing Signed URL w/ canned policy

* You need to generate the Signed URL and then download the file (look at [generate_presigned_url.py](helpers/generate_presigned_url.py) for details):

```shell
./helpers/generate_presigned_url.py --distribution <Distribution> --s3-key 'signed_urls/index.html' --private-key-file keys/SAPC01-DEFAULT-KEY --public-key-id <DefaultPublicKey>
curl 'https://d789bhp8twpdd.cloudfront.net/signed_urls/index.html?Expires=1615741015&Signature=IjSwz7Cfru~qOY00Xo5LFlpOFeX0ricTFe039wT6NOGo-3TN~wvQIgRwMNjpA-L7jTWS7GID3VTqsxH0eTNe9nFHlHxwWXFjg5e3v~IvocTNWNLhhOkL8cn0BDjWz0Tk-zMvs5-MRgg8MgPKrQKrgv6BGFenXErOFYqLTLNKBebfk3beWAYAwKU95S4STnaFBS15jUb-ZtSokc9KvrV5fFUUojWMpUtrKk87ZQLIj3YD0fcUjpz9cBfPPREtM4Ow~87PjKuJug11Te5dGefA6lUINuvxlLoDPrBJr5RgyZkVmkQvHZw1YHlmlio8uoSWKyyLTBPlTZlZI3mxyBLmJQ__&Key-Pair-Id=K2LNQ3JJCKNLZG'
<!doctype html><html lang="en"><body>This page is protected by Signed URLs</body></html>
```

### Testing Signed URL w/ custom policy

* You need to generate the Signed URL and then download the file (look at [generate_presigned_url.py](helpers/generate_presigned_url.py) for details):

*BEWARE*: be careful with your timezone

```shell
./helpers/generate_presigned_url.py --distribution <Distribution> --s3-key 'signed_urls/index.html' --expire 60 --private-key-file keys/SAPC01-DEFAULT-KEY --public-key-id <DefaultPublicKey> --use-custom --not-before=-3600 --not-after=3600
curl 'https://d789bhp8twpdd.cloudfront.net/signed_urls/index.html?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kNzg5YmhwOHR3cGRkLmNsb3VkZnJvbnQubmV0L3NpZ25lZF91cmxzL2luZGV4Lmh0bWwiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MTU3NDQ0MzJ9LCJEYXRlR3JlYXRlclRoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTYxNTczNzIzMn19fV19&Signature=eWyLsUii0zJMjkYnk4EAWKmYv20UhNe66zJk2orGP-A3XGAZ7Qbdja0WnA8JbZ3-GzGVVx4A70rkUi1lLkSJj0DM-RM0zCflQkgFJHVKuDD3j33OJtyh0vHzQPZw7~6CAwAiIKO5yxEE~cHQru6BrDdg6aPWGgqKr~wjTYQeZR~6y3gmg6VMAHPfACuMI6Wc17OrmTT2Fbjx6VBB-gspKNYcz-fgRaUdHybPis2RpwlrsU3N~pHgPKno4nh9mQhrJcQUSOlkrmjBKcAfu30HLBtPAxzu3r7BHM26-k4kmA-uxJCywOUczfwO99~kW1-ePaq7ElGqetKNoHd1k5U7EA__&Key-Pair-Id=K2LNQ3JJCKNLZG'
<!doctype html><html lang="en"><body>This page is protected by Signed URLs</body></html>
```

## Testing Signed Cookies

* Try to download the `signed_cookies/index.html` protected by Signed URLs and it will fail

```shell
curl https://<Distribution>/signed_cookies/index.html
<?xml version="1.0" encoding="UTF-8"?><Error><Code>MissingKey</Code><Message>Missing Key-Pair-Id query parameter or cookie value</Message></Error>
```

### Testing Signed Cookies

```shell
./helpers/generate_presigned_url.py --distribution <Distribution> --s3-key 'signed_urls/index.html' --expire 60 --private-key-file keys/SAPC01-DEFAULT-KEY --public-key-id <DefaultPublicKey> --set-cookie
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```shell
aws cloudformation delete-stack --stack-name SAPC01-SignedUrlCookies
```

## Details

*Author*: rostskadat
