#!/usr/bin/env python

import sys
from get_cert import get_cert_chain


def sign(filename: str):
    _cert, private_key = get_cert_chain(filename)

    with open(filename, 'rb') as src:
        with open(filename + ".sig", 'wb') as dst:
            dst.write(private_key.sign(
                src.read()
            ))
    print("[+] signed {}; the signature is at {}".format(filename, filename + ".sig"))

    # All set. No need to save private_key!


if __name__ == "__main__":
    sign(sys.argv[1])
