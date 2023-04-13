# IdFederationCognito

## Scenario

This sample show case different type of integration with external Identity Provider

The demonstrated methods are:
* SAML 2.0
* Web Identity Federation with Cognito
* Single Sign On

### SAML 2.0 

The `SAML2.0` scenario integrate [simplesamlphp](https://simplesamlphp.org/) as a `IdP` on the master account and use that `IdP` in a linked account.

The SAML 2.0 scenario follows more or less [this blog post](https://aws.amazon.com/blogs/security/enabling-federation-to-aws-using-windows-active-directory-adfs-and-saml-2-0/)

## Building

```bash
sam build 
sam deploy --no-fail-on-empty-changeset --no-confirm-changeset --tags "PLATFORM=SAPC01" 
``` 

## Testing

With SAM you can test your function locally:

```
sam local invoke --event events/events.json IdFederationCognitoFunction
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name IdFederationCognito
```


## References

* [blogs/security/how-to-create-saml-providers-with-aws-cloudformation](https://aws.amazon.com/blogs/security/how-to-create-saml-providers-with-aws-cloudformation/
)
* [blogs/security/aws-federated-authentication-with-active-directory-federation-services-ad-fs/](https://aws.amazon.com/blogs/security/aws-federated-authentication-with-active-directory-federation-services-ad-fs/)
