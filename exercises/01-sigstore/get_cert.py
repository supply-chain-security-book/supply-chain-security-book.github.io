#!/usr/bin/env python

import base64
import sys
import json
from typing import Tuple
import urllib.parse
import hashlib
import jwt
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
from requests_oauthlib import OAuth2Session

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

AUTH_TIMEOUT = 300

client_id = "sigstore"
client_secret = ""
redirect_uri = "http://localhost:3939"
auth_uri = "https://oauth2.sigstore.dev/auth/auth"
token_uri = "https://oauth2.sigstore.dev/auth/token"
userinfo_endpoint = "https://oauth2.sigstore.dev/auth/userinfo"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Callback handler to log the details of received OAuth callbacks"""

    def do_GET(self):
        self.server.oauth_callbacks.append(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<script>window.close()</script>")


class OAuthCallbackServer(HTTPServer):
    """Local HTTP server to handle OAuth authentication callbacks"""

    def __init__(self, server_address):
        self.oauth_callbacks = []
        HTTPServer.__init__(self, server_address, OAuthCallbackHandler)


def receive_oauth_callback(timeout):
    """Blocking call to wait for a single OAuth authentication callback"""
    server_address = ("", 3939)
    oauthd = OAuthCallbackServer(server_address)
    oauthd.timeout = timeout
    try:
        oauthd.handle_request()
    finally:
        oauthd.server_close()
    callback_path = oauthd.oauth_callbacks.pop()
    parsed_response = urllib.parse.urlparse(callback_path)
    query_details = urllib.parse.parse_qs(parsed_response.query)
    return query_details["code"][0], query_details["state"][0]


def get_cert_chain(filename: str) -> Tuple[bytes, Ed25519PrivateKey]:
    # 1. Retrive an ID token (with authorization flow + PKCE)
    oauth = OAuth2Session(client_id, client_secret,
                          redirect_uri=redirect_uri, scope=("openid", "email",))
    code_verifier = "ideally-this-value-should-be-random-but-im-lazy"
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(
        code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=", "")
    authorization_url, state = oauth.authorization_url(
        auth_uri, code_challenge=code_challenge, code_challenge_method="S256")

    print("[+] Visit the folowing URL for browser-based authentication...".format(AUTH_TIMEOUT))
    print("{}".format(authorization_url))

    authorization_code, cb_state = receive_oauth_callback(AUTH_TIMEOUT)
    if cb_state != state:
        msg = "Callback state {0!r} didn't match request state {1!r}"
        raise RuntimeError(msg.format(cb_state, state))

    session = oauth.fetch_token(
        token_uri,
        code=authorization_code,
        client_secret=client_secret,
        code_verifier=code_verifier,
    )
    id_token = session["id_token"]
    parsed_id_token = jwt.decode(id_token, options={
        "verify_signature": False,
    })
    print("[+] Got the following ID token:")
    print("{}".format(parsed_id_token))

    email = parsed_id_token["email"]
    print("[+] E-mail: {}".format(email))

    # 2. Generate a short-lived key pair on memory (i.e. *an ephermeral key*)
    private_key = Ed25519PrivateKey.generate()
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # 3. Generate a Certificate Signing Request (CSR)
    signed_email_address = private_key.sign(
        email.encode()
    )
    csr = {
        "publicKey": {
            "content":  base64.b64encode(public_key_pem).decode("utf8"),
            "algorithm": "ecdsa"
        },

        # Exercise (A): Why do we need this field?
        "signedEmailAddress": base64.b64encode(signed_email_address).decode("utf8"),
    }

    # 4. Send the CSR to Fulcio to get a certificate (chain)
    r = requests.post("https://fulcio.sigstore.dev/api/v1/signingCert", data=json.dumps(csr),  headers={
        # Exercise (B): Could the source of id_token arbitrary? In the other words, should public instances of Fulcio accept ID tokens from arbitrary IdPs?
        "authorization": f"Bearer {id_token}",
        "content-type": "application/json",
        "accept": "application/pem-certificate-chain",
    })

    print("[+] Got the following certificate (chain)!")

    with open(filename + ".crt", 'wb') as dst:
        dst.write(r.content)
    with open(filename + ".pub", 'wb') as dst:
        dst.write(public_key_pem)
    print("[+] saved the certificate chain as {} and the public key as {}".format(filename, filename + ".pub"))

    return r.content, private_key


if __name__ == "__main__":
    get_cert_chain(sys.argv[1])
