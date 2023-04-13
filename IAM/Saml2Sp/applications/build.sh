#!/bin/bash

repository_url=$1
if [ -z "${repository_url}" ]; then
    ECR_STACK_NAME=SAPC01-Saml2Sp-ecr
    repository_url=$(aws cloudformation describe-stacks --stack-name ${ECR_STACK_NAME} --query 'Stacks[0].Outputs[?@.OutputKey == `ContainerRepositoryUrl`].OutputValue' --output text)
fi
# BEWARE KEEP IN SYNC WITH template.yaml:Parameters/SubDomainName
# The application should be modified to get that at runtime instead...
export SP_URL_BASE=https://sapc01-saml2-sp.domain.com
export IDP_URL_BASE=https://sapc01-saml2-idp.domain.com

# without the idp reference
pushd flask-sp/sp-wsgi/ > /dev/null
echo "Generating provisional SP metadata ..."
IS_STANDALONE=True ../../tools/make_metadata.py sp_conf > ../../flask-idp/idp2/standalone_sp.xml
popd > /dev/null
# generate the real one
pushd flask-idp/idp2 > /dev/null
echo "Generating IdP metadata ..."
../../tools/make_metadata.py idp_conf > idp.xml
popd > /dev/null
# then the idp reference
pushd flask-sp/sp-wsgi/ > /dev/null
echo "Generating definitive SP metadata ..."
cp ../../flask-idp/idp2/idp.xml .
../../tools/make_metadata.py sp_conf > sp.xml
popd > /dev/null

$(aws ecr get-login --no-include-email)
docker build -t "${repository_url}:latest-flask-sp" flask-sp
docker build -t "${repository_url}:latest-flask-idp" flask-idp
docker push "${repository_url}:latest-flask-sp"
docker push "${repository_url}:latest-flask-idp"
