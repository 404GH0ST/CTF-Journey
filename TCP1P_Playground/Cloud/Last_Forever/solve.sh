#!/bin/bash

if [ -f ./out.txt ]; then
	rm ./out.txt
fi

keyword="myheart.txt"
bucket="forever.lychnobyte.my.id"
version_ids=$(aws s3api list-object-versions --bucket $bucket --no-sign-request | grep "$keyword" -A 1 | grep -o '"VersionId": "[^"]*' | sed 's/"VersionId": "//' | tail +2)

for versionid in $version_ids; do
	curl -s "http://$bucket"".s3.amazonaws.com""/$keyword?versionId=$versionid" >>out.txt
done

cat out.txt | tr -d "\n" | rev
