# Worksheet   : Testing Methodology
# Author      : Amihai Ben-Arush
# Code review :
# Description : Test unit to check if a site is reachable
#!/bin/bash
response=$(curl --write-out '%{http_code}' --connect-timeout 3 --silent --output /dev/null $1)
if [[ $response == '000' ]]; then
	echo 'website is unreachable'
	exit 6
else
	echo "website is reachable, status code '$response'"
	exit 0
fi
