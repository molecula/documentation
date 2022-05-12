---
id: data-directory-structure
title: Data Directory Structure
sidebar_label: Data Directory Structure
---

In FeatureBase version 3.x, the data directory structure was updated to account for the new implementation of roaring B-tree format and etcd being used to manage key/value store. 

In general, the Molecula team would like to discourage reliance on any particular details of the directory structure.

FeatureBase v3.x:
```
$ tree -d -L 3 .pilosa/
./
├── disco
│   └── member
│       ├── snap
│       └── wal
└── indexes
    ├── bank
    │   ├── _keys
    │   ├── backends
    │   └── fields
    ├── dell
    │   ├── backends
    │   └── fields
    └── dell2
        ├── backends
        └── fields
```

 - `disco` directory is used to store etcd data.
 - `idalloc.db` stores tracking information for any indexes that are using the ID auto-generation functionality provided in some ingesters. 
 - `indexes` is the main data directory containing a subdirectory for each table in FeatureBase. 
    - If index is using string keys, then there will be a `_keys` directory, which contains a translation file for each partition this node is responsible for. 
    - The `fields` subdirectory encodes some metadata about the fields which exist. It also contains key translation files for the fields using key translation.
    - The `backends` subdirectory contains the actual bitmap data.
- `startup.log` contains the FeatureBase versions that has been run for this data directory.




