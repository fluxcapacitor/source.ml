#!/usr/bin/env bash

# Generate Private Key, Certificate and PEM
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt \
-subj "/C=US/ST=California/L=San Francisco/O=Pipeline.IO/CN=*.pipeline.io/emailAddress=chris@fregly.com"
sudo openssl x509 -noout -fingerprint -text < tls.crt > tls-wildcard.info
sudo cat tls.crt tls.key > tls.pem