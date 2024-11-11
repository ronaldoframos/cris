#!/bin/bash

# 1. Gerar chave privada RSA
openssl genrsa -out private_key.pem 2048

# 2. Criar arquivo de configuração para o certificado
cat > cert_config.cnf << EOL
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
x509_extensions = v3_req

[dn]
C=BR
ST=Seu Estado
L=Sua Cidade
O=Sua Organizacao
OU=Desenvolvimento
CN=localhost
emailAddress=seu.email@exemplo.com

[v3_req]
subjectAltName = @alt_names
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
EOL

# 3. Gerar o certificado autoassinado
openssl req -new -x509 -sha256 -nodes -days 365 \
    -key private_key.pem \
    -out certificate.pem \
    -config cert_config.cnf
