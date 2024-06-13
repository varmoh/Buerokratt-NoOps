#!/bin/bash

# Generate CA private key
openssl genrsa -out ca-key.pem 4096

# Generate CA certificate signing request (CSR)
openssl req -new -key ca-key.pem -out ca-csr.pem -subj "/CN=bykCA"

# Self-sign the CA certificate
openssl x509 -req -days 3650 -in ca-csr.pem -signkey ca-key.pem -out ca.pem

# Clean up intermediate files
rm ca-csr.pem
