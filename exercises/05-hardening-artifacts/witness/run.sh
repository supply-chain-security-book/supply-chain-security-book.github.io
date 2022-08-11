#!/bin/sh

# ignore me
openssl genpkey -algorithm ed25519 -outform PEM -out testkey.pem
openssl pkey -in testkey.pem -pubout > testpub.pem

# 本質
witness sign -f policy.json --key testkey.pem --outfile policy-signed.json
KO_DOCKER_REPO=ttl.sh witness run -- ko build ./

# ignore me
rm testkey.pem testpub.pem
