#!/usr/bin/env bash
#
# FILE: create_zip_for_eb.sh
#
# DESCRIPTION: This is a simple script to create a ZIP file that can be deployed in an ElasticBeanstalk Environment
#
pushd $(dirname $0)
artifact=flask-hello-world.zip
[ ! -d build/.ebextensions ] && mkdir -p build/.ebextensions
rm -f build/${artifact}
cp -r src/* build
cp -r ebextensions/* build/.ebextensions
cd build 
pip3 install --upgrade --requirement requirements.txt --target .
zip -r ${artifact} * .[^.]*
popd