# Hardening Artifacts

Given all sources including dependency definitions are trusted, and the sourcces produced artifacts without lacking dependency information as possible, but we have still some challenges.
One of the major challenges is that **the artifact does not include neither who generated the artifacts nor when and how the artifacts was made.**

- **who**: In the last chapter, you built some container images. You know you yourself built, but others can't know that in general. What if a container running in production environments is suspicious and one gets worried about who generated the image?
- **when and how**: Your containers in the last chapters were built by `ko` and `apko`. What if a specific version of `ko` has a malicious function to inject a backdoor to containers? The SBoM doesn't include tooling information though!

## Preliminaries

Run the following commands to install requirements:

```sh
go install github.com/google/go-containerregistry/cmd/crane@v0.11.0
go install github.com/sigstore/cosign/cmd/cosign@v1.10.1
```

## Container Signing

### Sign Container Images by Cosign

`cosign` allows us to give a signature to a container image. The signature lets us to verify who signed the container.
To sign the image with an ephemeral key + Fulcio, you can use `cosign sign` command as follows:

```sh
# Generate an image to sign + Sign the image with an ephemeral key

# in fish
set IMAGE_NAME ttl.sh/(uuidgen | tr [:upper:] [:lower:]):4h
docker run -v "$PWD":/work distroless.dev/apko build src/alpine-base.yaml $IMAGE_NAME apko-alpine.tar
crane push apko-alpine.tar $IMAGE_NAME

set IMAGE_NAME_HASHED $IMAGE_NAME@(crane digest $IMAGE_NAME)
COSIGN_EXPERIMENTAL=1 cosign sign $IMAGE_NAME_HASHED


# in bash
IMAGE_NAME=ttl.sh/$(uuidgen | tr [:upper:] [:lower:]):4h
docker run -v "$PWD":/work distroless.dev/apko build src/alpine-base.yaml $IMAGE_NAME apko-alpine.tar
crane push apko-alpine.tar $IMAGE_NAME

IMAGE_NAME_HASHED=$IMAGE_NAME@$(crane digest $IMAGE_NAME)
COSIGN_EXPERIMENTAL=1 cosign sign $IMAGE_NAME
```

To verify the signature, run the following:

```sh
COSIGN_EXPERIMENTAL=1 cosign verify $IMAGE_NAME_HASHED | jq
```

We reviewed the following problem, but now your colleagues may heave a sigh of relief once they find your signature in the image!

> What if a container running in production environments is suspicious and one gets worried about who generated the image?

### Exercise (optional): Cosign Internals

What's happening behind signing process by Cosign? What does the command `cosign verify` actually verify?

## Software Attestation

### Overvivew

_A software attestation_ is an authenticated statement about a software artifact or collection of software artifacts. Here's an example of attestations quoted from SLSA docs:

![Quoted from SLSA docs](https://github.com/slsa-framework/slsa/raw/main/docs/images/attestation_example_english.svg)

The figure includes some unfamiliar words. Let's check definitions:

> ![Quoted from SLSA docs](https://github.com/slsa-framework/slsa/raw/main/docs/images/attestation_layers.svg)
>
> - **Artifact:** Immutable blob of data described by an attestation, usually
>   identified by cryptographic content hash. Examples: file content, git
>   commit, container digest. May also include a mutable locator, such as
>   a package name or URI.
> - **Attestation:** Authenticated, machine-readable metadata about one or more
>   software artifacts. An attestation MUST contain at least:
>   - **Envelope:** Authenticates the message. At a minimum, it MUST contain:
>     - **Message:** Content (statement) of the attestation. The message
>       type SHOULD be authenticated and unambiguous to avoid confusion
>       attacks.
>     - **Signature:** Denotes the **attester** who created the attestation.
>   - **Statement:** Binds the attestation to a particular set of artifacts.
>     This is a separate layer to allow for predicate-agnostic processing
>     and storage/lookup. MUST contain at least:
>     - **Subject:** Identifies which artifacts the predicate applies to.
>     - **Predicate:** Metadata about the subject. The predicate type SHOULD
>       be explicit to avoid misinterpretation.
>   - **Predicate:** Arbitrary metadata in a predicate-specific schema. MAY
>     contain:
>     - **Link:** _(repeated)_ Reference to a related artifact, such as
>       build dependency. Effectively forms a [hypergraph] where the
>       nodes are artifacts and the hyperedges are attestations. It is
>       helpful for the link to be standardized to allow predicate-agnostic
>       graph processing.
> - **Bundle:** A collection of Attestations, which are usually but not
>   necessarily related.
> - **Storage/Lookup:** Convention for where attesters place attestations and
>   how verifiers find attestations for a given artifact.

Once Attestations

### Predicate: `https://spdx.dev/Document`

First, build a container image with `apko`:

```sh
# Generate an image to sign + Sign the image with an ephemeral key

# in fish
set IMAGE_NAME ttl.sh/(uuidgen | tr [:upper:] [:lower:]):4h
docker run -v "$PWD":/work distroless.dev/apko build src/alpine-base.yaml $IMAGE_NAME apko-alpine.tar
crane push apko-alpine.tar $IMAGE_NAME

# in bash
IMAGE_NAME=ttl.sh/$(uuidgen | tr [:upper:] [:lower:]):4h
docker run -v "$PWD":/work distroless.dev/apko build src/alpine-base.yaml $IMAGE_NAME apko-alpine.tar
crane push apko-alpine.tar $IMAGE_NAME
```

Then you'll see `sbom-*.spdx.json` in the current directory. You can attest it to the container image by the following commands:

```sh
COSIGN_EXPERIMENTAL=1 cosign attest $IMAGE_NAME --predicate sbom-*.spdx.json --type spdxjson
```

To see the attestation(s), run the following:

```sh
cosign download attestation $IMAGE_NAME
```

To verify the attestation(s), run the following:

```sh
COSIGN_EXPERIMENTAL=1 cosign verify-attestation $IMAGE_NAME --type spdxjson
```

https://docs.sigstore.dev/cosign/attestation/

### Exercise (optional): Cosign Internals

What's happening behind attestation process by Cosign? What does the command `cosign verify-attestation` actually verify?

### Exercise (optional): Attest More!

A tool [witness](https://github.com/testifysec/witness) allows you to generate more attestations on build.

### Exercise: Work with Trivy


```sh
# 適当に含まれている脆弱性検査をしたいイメージを用意する

# in bash or zsh
docker pull alpine:3.10
set IMAGE_NAME ttl.sh/$(uuidgen | tr "[:upper:]" "[:lower:]"):8h
docker tag alpine:3.10 $IMAGE_NAME
docker push $IMAGE_NAME

# in fish
docker pull alpine:3.10
set IMAGE_NAME ttl.sh/(uuidgen | tr [:upper:] [:lower:]):8h
docker tag alpine:3.10 $IMAGE_NAME
docker push $IMAGE_NAME
```

```sh
# Canary 版 Trivy を拾ってくる（最新のリリースに機能が含まれていないため……）
# https://github.com/aquasecurity/trivy/actions/runs/2832002363

# Trivy で脆弱性情報をスキャンする
trivy image --format cosign-vuln --output vuln.json $IMAGE_NAME

# スキャンして出てきた結果をイメージに attest する
COSIGN_EXPERIMENTAL=1 cosign attest --type vuln --predicate vuln.json $IMAGE_NAME

# attestation を verify する
COSIGN_EXPERIMENTAL=1 cosign verify-attestation $IMAGE_NAME --type vuln
```

## Continuous Review of SBoM

> **Info**
> Coming soon!
