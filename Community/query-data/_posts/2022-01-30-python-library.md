---
title: Python Client Library
---


## Client

A basic usage example of the Python client is shown below. Details about PQL query syntax can be found on the [PQL Introduction](/pql-guide/pql-introduction) page.


```python
    import molecula

    # create client
    client = molecula.Client('host:port', auth=molecula.TLSAuth(certificate, private_key))

    # create VDS
    client.create_vds(vdsd='')

    # list VDSs
    client.get_vds_list()

    # get VDS
    client.get_vds(name='vds-name')

    # delete VDS
    client.delete_vds(name='vds-name')

    # query a VDS (PQL)
    print(list(client.query("vds-name", "PQL query")))

    # query a VDS (SQL)
    print(list(client.querysql("SQL query")))

    # concurrent futures
    future1 = client.query_future("vds-name", "PQL query")
    future2 = client.query_future("vds-name", "PQL query")
    print(future1.result())
    print(future2.result())

    # futures with SQL
    future1 = client.querysql_future("SQL query")
    future2 = client.querysql_future("SQL query")
    print(future1.result())
    print(future2.result())

    # inspect record
    print(list(client.inspect("vds-id", ids=[100, 101], fields=["field-name"])))
```

### Connecting to a Cluster

Client-side load balancing with failover is supported via the underlying library, gRPC Core. In order to use this feature, you must configure the client address with a compatible name as defined in the [gRPC Name Resolution](https://grpc.github.io/grpc/core/md_doc_naming.html) document. The name can resolve to multiple hosts, and those hosts will be used with a client-side Round Robin load balancer, which will automatically remove inactive hosts.

For example, in order to connect to two hosts named `10.1.100.1` and `10.1.100.2`, you would chose the `ipv4` scheme as defined in the gRPC Name Resolution document, and instantiate the client:

```python
client = molecula.Client('ipv4:10.1.100.1:20101,10.1.100.2:20101')
```

Similarly, you can use the above connection string with `pilosa-cli`:

```python
pilosa-cli ipv4:10.1.100.1:20101,10.1.100.2:20101 get-vds-list
```
