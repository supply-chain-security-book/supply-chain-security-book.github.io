# Play with Cosign

## Preliminaries

### Install Cosign & Crane

Run the following commands:

```sh
go install github.com/google/go-containerregistry/cmd/crane@latest
go install github.com/sigstore/cosign/cmd/cosign@v1.10.1
```

### Build a Docker image

Run the following commands to build a sample docker image:

```sh
# in bash
IMAGE_NAME=ttl.sh/$(uuidgen | tr [:upper:] [:lower:]):4h
docker build ./src -t $IMAGE_NAME
docker push $IMAGE_NAME

# in fish
set IMAGE_NAME ttl.sh/(uuidgen | tr [:upper:] [:lower:]):4h
docker build -t $IMAGE_NAME ./src
docker push $IMAGE_NAME
```

## Try Cosign

To sign the image with an ephemeral key, you can use `cosign sign` command as follows:

```sh
# in bash
IMAGE_NAME_HASHED=$(docker inspect $IMAGE_NAME | jq -r ".[0].RepoDigests[0]")
COSIGN_EXPERIMENTAL=1 cosign sign $IMAGE_NAME_HASHED

# in fish
set IMAGE_NAME_HASHED (docker inspect $IMAGE_NAME | jq -r ".[0].RepoDigests[0]")
COSIGN_EXPERIMENTAL=1 cosign sign $IMAGE_NAME_HASHED
```

To verify the signature, run the following:

```sh
COSIGN_EXPERIMENTAL=1 cosign verify $IMAGE_NAME_HASHED | jq
```

## Cosign Internals

Coming soon!
