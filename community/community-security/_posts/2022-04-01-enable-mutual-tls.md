---
id: enable-mutual-tls
title: How To Enable Mutual TLS
sidebar_label: Enable Mutual TLS
---

## TLS/Encryption

FeatureBase supports Mutual TLS, which allows both the client and server to cryptographically verify each other and establish an encrypted connection. To enable encryption on every connection, FeatureBase is configured with a PEM-encoded TLS keypair. In addition, nodes in a FeatureBase cluster internally communicate over the Memberlist protocol, which can be configured with a shared 32-bit key to enable AES-256 symmetric encryption within the cluster.


### Generating keys

In order to enable TLS, you will need to generate a TLS keypair for FeatureBase. For testing in a development environment, we recommend using [Certstrap](https://github.com/square/certstrap) to generate the necessary keys. **We do not recommend certstrap for production usage.** Setting up a secure public key infrastructure is outside of the scope of this document, but the following examples will use Certstrap to bootstrap a certificate authority and create signed TLS keypairs for the purpose of demonstration.

Create a root CA for testing purposes:


```shell
    certstrap init --common-name "auth.mybusiness.com"
```


Create and sign a keypair for FeatureBase:


```shell
    certstrap request-cert --common-name "featurebase.mybusiness.com"
    certstrap sign featurebase.mybusiness.com --CA auth.mybusiness.com
```


Create a 32-bit key to encrypt Memberlist (gossip) communication:


```shell
    head -c 32 /dev/random > out/gossip.key
```


After running the previous commands, you should have the following files in a directory called “out”:


```text
    auth.mybusiness.com.crl
    auth.mybusiness.com.crt
    auth.mybusiness.com.key
    featurebase.mybusiness.com.crt
    featurebase.mybusiness.com.csr
    featurebase.mybusiness.com.key
    gossip.key
```



### Configuring FeatureBase

FeatureBase must be configured with the certificate and private key using environment variables, a configuration file, or command line parameters. Internal etcd cluster communication does not currently support TLS, but that's coming soon.


```toml
    [tls]
      certificate = "/path/to/featurebase.mybusiness.com.crt"
      key = "/path/to/featurebase.mybusiness.com.key"
```

You must also update your bind configuration to use the `https` scheme.


```toml
bind = "https://YOUR-DOMAIN-HERE:10101"
bind-grpc = "https://YOUR-DOMAIN-HERE:20101"
```
