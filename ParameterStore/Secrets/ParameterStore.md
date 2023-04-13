# From `Parameters` Section

* LinuxImageId=`ami-0bb3fad3c0286ebd5`
* WindowsImageId=`ami-0b65c1813d92cc713`

# From `AWS::SSM::Parameters` in Resources Section

* LinuxImageParameter (`CFN-LinuxImageParameter-nOjrzzgOyjhD`) =`ami-0bb3fad3c0286ebd5`
* WindowsImageParameter (`CFN-WindowsImageParameter-AGF77QrbYwTh`) =`ami-0b65c1813d92cc713`

# Indirectly: 

* PlainTextParameterStoreSecureString (`CFN-PlainTextParameterStoreSecureString-2sUZ9ApeDq99`) = `{resolve:ssm-secure:ParameterStoreSecureString:1}`
* PlainTextSecretsManagerSecret (`CFN-PlainTextSecretsManagerSecret-47PmE3ESTheX`) = `Passw0rd`
* SecretsManagerSecret = `{\{resolve:ssm-secure:/aws/reference/secretsmanager/SecretsManagerSecret}\}`          

# Resolved inline:

* LinuxImageId=`ami-0bb3fad3c0286ebd5`
* WindowsImageId=`ami-0b65c1813d92cc713`

# Different parameter type:

* StringParameter = StringParameterValue
* StringListParameter = StringListParameterValue1,StringListParameterValue2

# Using `SecretsManager`:

*BEWARE*, the construct `{\{resolve:ssm-secure:ParameterStoreSecureString:1}\}` fails on Custom Resource

*BEWARE*, the construct `{\{resolve:secretsmanager:SecretsManagerSecret:SecretString:password}\}` will not work.
