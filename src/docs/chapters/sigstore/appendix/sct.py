#!/usr/bin/env python

import sys
from cryptography.x509 import (
    PrecertificateSignedCertificateTimestamps,
    load_pem_x509_certificate,
)


def main():
    with open(sys.argv[1], 'r') as f:
        crt = f.read()

    # Try to retrieve the embedded SCTs within the cert.
    raw_cert = b"-----BEGIN CERTIFICATE-----" + \
        crt.split("-----BEGIN CERTIFICATE-----")[1].encode()
    print(raw_cert)
    cert = load_pem_x509_certificate(raw_cert)
    precert_scts_extension = cert.extensions.get_extension_for_class(
        PrecertificateSignedCertificateTimestamps
    ).value

    print("SCT: {}".format(precert_scts_extension[0]))

    # TODO: verify SCT by yourself
    # You'll need https://rekor.sigstore.dev/api/v1/log/publicKey in the verification.


if __name__ == "__main__":
    main()
