#!/bin/bash
set -euo pipefail

BITCOIN_VERSION="26.0"
BITCOIN_ARCHIVE="bitcoin-${BITCOIN_VERSION}-x86_64-linux-gnu.tar.gz"
BITCOIN_URL="https://bitcoincore.org/bin/bitcoin-core-${BITCOIN_VERSION}/${BITCOIN_ARCHIVE}"
BITCOIN_SHA256="2a6cca634f9cd5c4f9d3b6947d3cfc89da7afaf6c80322f0de0d7572c63a5cf8"

sudo apt update -y && sudo apt install -y curl
curl --fail --location --silent --show-error -o /tmp/bitcoin.tar.gz "${BITCOIN_URL}"
printf '%s  %s\n' "${BITCOIN_SHA256}" /tmp/bitcoin.tar.gz | sha256sum -c -

sudo tar -xf /tmp/bitcoin.tar.gz -C /
sudo mv /bitcoin-26.0 /bitcoin

# Add bitcoin binaries to path
export PATH=/bitcoin/bin:$PATH
