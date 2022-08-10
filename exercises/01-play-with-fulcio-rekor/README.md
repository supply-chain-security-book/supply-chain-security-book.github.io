# Fulcio + Rekor the Hardway

In this section, you'll interact with Fulcio and Rekor by a small Python script. This kind of interaction is tricky a little bit --- in general, you won't talk with them directly and use wrappers like Cosign or any other attestators.

## Play with Fulcio

Where you should start is installation of requirements:

```sh
pip install -r requirements.txt
```

Once you have installed all requirements successfully, you can get a cert for an ephemeral key from Fulcio as follows:

```sh
python get_cert.py test
```

To see the content of the cert, use `openssl` as follows:

```sh
# Check the issued certificate
openssl x509 -in test.crt -text
```

## Play with Rekor

### Preliminaries

First of all, you need to install `rekor-cli`:

```sh
# with go
go install -v github.com/sigstore/rekor/cmd/rekor-cli@latest

# with prebuilt binary
echo "Visit https://github.com/sigstore/rekor/releases and download a rekor-cli binary you'd like"
```

### Sign `artifact.txt` with Ephemeral Keys

After the installation, you can generate the signature for `artifact.txt` as follows:

```sh
python sign.py artifacts/artifact.txt
```

You'll see `artifact.txt.sig` (the signature) and `artifact.txt.crt` (the certificate including a public key for the signature) in your local directory.
Upload the cert and the signature to public Rekor instance:

```sh
rekor-cli upload \
  --artifact artifacts/artifact.txt \
  --signature artifacts/artifact.txt.sig \
  --public-key artifacts/artifact.txt.crt \
  --pki-format x509
```

Then you'll see logs like:

```
Created entry at index 33612, available at:
    https://rekor.sigstore.dev/api/v1/log/entries/<uuid>
```

...and you can see the record in Rekor as follows:

```sh
# see raw logs
curl https://rekor.sigstore.dev/api/v1/log/entries/<uuid>

# see structured logs
rekor-cli get --uuid=<uuid>
```

### Verify Locally

You can verify the signature with the public key (regardless of the certificate's expiry date):

```sh
openssl dgst -sha256 \
  -verify artifacts/artifact.txt.pub \
  -signature artifacts/artifact.txt.sig \
  artifacts/artifact.txt
```

### Challenges

Let's dive into the details!

### Challenge 1 -- Find who signed

Has anyone signed `artifacts/sample.txt` and saved the signature at Rekor ever? If theere is, who is it?

> **info**
> You'll do this kind of inspection when you'd like to review the signer of an artifact.

### Challenge 2 -- Find what one has signed so far

`takashi.yoneuchi@shift-js.info` at GitHub was hacked via password breaches. Someone might have signed resources with containers.
Find the Rekor records related to `takashi.yoneuchi@shift-js.info` to find out invalid signatures!

> **info**
> You'll do this kind of inspection when an OIDC identity or OIDC provider is compromised or when public Fulcio instance is compromised.
