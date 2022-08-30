---
title: Installing FeatureBase
---

This document contains instructions for manually installing FeatureBase on a single node.

## Linux with systemd

**NOTE:** 
For FeatureBase 4.4.0 or later

### Install FeatureBase and Consumers

Extract the Molecula tarball.

Copy binaries to `/usr/local/bin/`, being sure to choose the correct binaries for your OS
 and CPU architecture, typically linux-amd64 for Linux:

- `featurebase`
- `molecula-consumer/*`

Copy files, and confirm settings are correct:
- configuration file `featurebase.conf` to `/etc/`
- service file `featurebase.service` to `/etc/systemd/system/`

Sample setup files are provided [below](#sample-files).

Create user `molecula` using a secure password:

```shell
adduser molecula
```

Create a log folder:

```shell
sudo mkdir /var/log/molecula
```

Change the ownership of the log folder to `molecula`:

```shell
sudo chown molecula /var/log/molecula
```

Create a data folder:

```shell
sudo mkdir -p /opt/molecula/featurebase
```

Change the ownership of the data folder to `molecula`:

```shell
sudo chown molecula /opt/molecula/featurebase
```

Refresh systemd so the services will load:

```shell
systemctl daemon-reload
```


Start FeatureBase services:

- `sudo systemctl start featurebase`
- `sudo systemctl enable featurebase`

Verify startup:

- `sudo systemctl status featurebase`

Inspect Logs:

- `journalctl -u featurebase -r`

Install the postgres client for psql:

```shell
sudo apt-get install postgresql-client
```

or

```shell
sudo yum install postgresql
```


### Test the Installation via HTTP

Running this command:
```shell
curl localhost:10101
```

Should result in output similar to this:

```text
Welcome. FeatureBase is running. Visit https://docs.featurebase.com for more information.
```

Running this command:

```shell
curl localhost:10101/status
```

Should result in output similar to this:

```json
{"state":"NORMAL","nodes":[{"id":"fbd5bdca-b741-4e2d-ad1d-e033fe0d91a2","uri":{"scheme":"http","host":"10.0.0.3","port":10101},"grpc-uri":{"scheme":"grpc","host":"10.0.0.3","port":20101},"isCoordinator":true,"state":"READY"}],"localID":"fbd5bdca-b741-4e2d-ad1d-e033fe0d91a2"}
```


#### Test the Installation via Postgres 

Running this command:
```shell
psql -h localhost -p 55432 -c "show tables;"
```

Should result in output similar to this:

```text
 Table
-------
 user
(1 row)
```


### Install Python Library

With Python3 available, install dependencies.

For Red Hat:

```shell
yum install python-devel
yum install gcc-c++
```

For Debian:

```shell
sudo apt-get update
sudo apt-get install python-dev-is-python3
sudo apt-get install build-essential
sudo apt install python3-pip
```

Install the python-molecula whl file:

```shell
pip3 install molecula-1.5.2-py3-none-any.whl
```

#### Test the Python installation

In a python3 script or REPL, this line should succeed if the installation completed:

```python
import molecula
```

To verify the connection to the VDSM, try to retrieve the VDS list:
```python
client = molecula.Client('localhost:20101')
for vds in client.get_vds_list():
    print(vds)
```

## MacOS

**NOTE:** 
For Molecula 2.1.1

**IMPORTANT:**
As with many data stores, FeatureBase requires open file limits to be increased from their defaults. Managing open file limits changes frequently with MacOS versions. Here are a few resources to consult:

- [max-file-count configuration option](/setting-up-featurebase/enterprise/featurebase-configuration#max-file-count)
- https://gist.github.com/tombigel/d503800a282fcadbee14b537735d202c
- https://docs.riak.com/riak/kv/latest/using/performance/open-files-limit/index.html#mac-os-x-el-capitan
:::

Extract the Molecula tarball.

Copy binaries to `/usr/local/bin/`, being sure to choose the correct binaries for your OS
 and CPU architecture, typically darwin-amd64 for MacOS.

- `featurebase`
- `molecula-consumer/*`

Copy file, and confirm settings are correct:

- configuration file `featurebase.conf` to `/etc/`:

Sample setup files are provided [below](#sample-files).

Create a log folder:

```shell
sudo mkdir /var/log/molecula
```

Change the ownership of the log folder to your username:

```shell
sudo chown $USER /var/log/molecula
```

Create a data folder:

```shell
sudo mkdir -p /opt/molecula/featurebase
```

Start FeatureBase apps as background processes:
- `featurebase server -c /etc/featurebase.conf &`

Install a postgres client for psql. We recommend installing via Homebrew:

```shell
brew install postgresql
```


### Test the Installation via HTTP

Running this command:
```shell
curl localhost:10101
```

Should result in output similar to this:

```text
Welcome. FeatureBase is running. Visit https://docs.featurebase.com for more information.
```

Running this command:

```shell
curl localhost:10101/status
```

Should result in output similar to this:

```json
{"state":"NORMAL","nodes":[{"id":"fbd5bdca-b741-4e2d-ad1d-e033fe0d91a2","uri":{"scheme":"http","host":"10.0.0.3","port":10101},"grpc-uri":{"scheme":"grpc","host":"10.0.0.3","port":20101},"isCoordinator":true,"state":"READY"}],"localID":"fbd5bdca-b741-4e2d-ad1d-e033fe0d91a2"}
```


#### Test the Installation via Postgres 

Running this command:
```shell
psql -h localhost -p 55432 -c "show tables;"
```

Should result in output similar to this:

```text
 Table
-------
 user
(1 row)
```


### Install Python Library

```shell
unzip python-molecula-1.7.0.zip
cd python-molecula-1.7.0
python3 setup.py install
```


#### Test the Python installation

In a python3 script or REPL, this line should succeed if the installation completed:

```python
import molecula
```


To verify the connection to the VDSM, try to retrieve the VDS list:
```python
client = molecula.Client('localhost:20101')
for vds in client.get_vds_list():
    print(vds)
```

## Software Configuration

Refer [Host System](/reference/operations/enterprise/hostsystem) for commonly encountered issues and operations checklist.

## Sample Files


### for Amazon Linux version 2
In an AMI on EC2, in region us-east-2

```text
[Unit]
After=network.target
Description=Service for FeatureBase
Documentation=https://docs.featurebase.com/
DefaultDependencies=no

[Service]
EnvironmentFile=
ExecStart=/usr/local/bin/featurebase server -c /etc/featurebase.conf
Restart=on-failure
RestartSec=30
User=molecula

[Install]
WantedBy=multi-user.target
```


### existing

featurebase.conf:
```toml
name = "pilosa1"
bind = "0.0.0.0:10101"
bind-grpc = "0.0.0.0:20101"

data-dir = "/opt/molecula/featurebase"
log-path = "/var/log/molecula/featurebase.log"

max-file-count=900000
max-map-count=900000

long-query-time = "10s"

[postgres]

    bind = "localhost:55432"

[cluster]

    name = "cluster1"
    replicas = 1

[etcd]

    listen-client-address = "http://localhost:10401"
    listen-peer-address = "http://localhost:10301"
    initial-cluster = "pilosa1=http://localhost:10301"

[metric]

    service = "prometheus"
```

featurebase.service:
```text
# Not Ansible managed

[Unit]
Description="Service for FeatureBase"

[Service]
RestartSec=30
Restart=on-failure
EnvironmentFile=
User=molecula
ExecStart=/usr/local/bin/featurebase server -c /etc/featurebase.conf


[Install]
```
