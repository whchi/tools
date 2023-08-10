#!/bin/bash
# Set the domain name variable (replace with your domain)
DOMAIN_NAME="$1"
# Check if the domain name is provided
if [ -z "$DOMAIN_NAME" ]; then
  echo "Please provide a domain name as an argument."
  exit 1
fi
# Create a private key without passphrase
openssl genpkey -algorithm RSA -out "${DOMAIN_NAME}.key"

# Set appropriate permissions
chmod 400 "${DOMAIN_NAME}.key"

# Create a certificate signing request (CSR)
openssl req -new -key "${DOMAIN_NAME}.key" -out "${DOMAIN_NAME}.csr" -subj "/C=US/ST=State/L=Location/O=Organization/OU=Unit/CN=${DOMAIN_NAME}"

# Self-sign the CSR to create the certificate
openssl x509 -req -days 365 -in "${DOMAIN_NAME}.csr" -signkey "${DOMAIN_NAME}.key" -out "${DOMAIN_NAME}.crt"

# Print success message
echo "Self-signed SSL certificate and key created for domain: ${DOMAIN_NAME}"

# Optional: Print the certificate
openssl x509 -in "${DOMAIN_NAME}.crt" -text -noout

# Clean up the CSR
rm "${DOMAIN_NAME}.csr"
