#!/bin/bash
response=$(curl --write-out '%{http_code}' --connect-timeout 3 --silent --output /dev/null $1)
if [[ $response == '000' ]]; then
	echo 'website is unreachable'
else
	echo "website is reachable, status code '$response'"
fi
