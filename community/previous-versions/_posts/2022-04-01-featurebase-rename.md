---
id: featurebase-rename
title: FeatureBase Rename
sidebar_label: FeatureBase Rename
---


As of Molecula 5.0, the core product formerly known as Pilosa will be renamed to FeatureBase. This change extends to several interfaces, so a few additional steps are required when upgrading from pre-5.0 to post-5.0. The 4.4 release includes an option to switch to the FeatureBase name early.

Previously, the Molecula *release version* and the Pilosa *server version* numbers were out of sync by one major version. For example, Molecula 4.3 includes Pilosa 3.3. Rather than advancing from Pilosa 3.x to FeatureBase 4.0, FeatureBase will skip the 4.x series, and the first major version will be 5.0. The distinct *release version* will no longer exist. At the same time, ingester and client versions will update to 5.0 as well.

Note that the term "FeatureBase" may be visible in some logs and error messages prior to the 5.0 release, and "Pilosa" may still be visible after the 5.0 release.


## Binary name change
Starting with the 4.4 release the binary will be named `featurebase` rather than `pilosa`. Any shell scripts, service definition files, or similar references to the binary, should be updated to reflect this. During this transition, it may be helpful to define a symlink to the `featurebase` binary named `pilosa`.


## Configuration

Some configuration parameters previously included the word "pilosa". For 5.0 releases, these previous parameters will continue to work, as aliases for the new names, replacing "pilosa" with "featurebase". Starting with version 6.0, the "pilosa" aliases will no longer be available.

For future 4.x releases, FeatureBase [metrics](/community/community-monitoring/monitoring#metrics) will continue to use the "pilosa" namespace. Optionally, the "featurebase" namespace can be used, by using the `--future.rename` configuration parameter. Starting with version 5.0, the "featurebase" namespace will be used by default.

The default data directory will switch from `~/.pilosa` to `/opt/molecula/featurebase`, and the default node name will switch from `pilosa0` to `featurebase0`.


### FeatureBase

In Molecula version 4.4 (Pilosa version 3.4) and later, until the next major release (FeatureBase 5.0), the optional boolean configuration parameter `--future.rename` is available. It has the following effects:

- Switches the prefix that is used by [environment variables](/community/community-setup/featurebase-configuration) for configuring FeatureBase from `PILOSA` to `FEATUREBASE`. For example, `PILOSA_DATA_DIR` becomes `FEATUREBASE_DATA_DIR`. Note that the `--future.rename` flag can be specified as an environment variable with `PILOSA_FUTURE_RENAME`, but not `FEATUREBASE_FUTURE_RENAME`.
- Switches the metrics namespace (the prefix of the metric names reported by Prometheus or other metrics services) from "pilosa" to "featurebase". For example, the Prometheus metric `pilosa_maximum_shard` becomes `featurebase_maximum_shard`.
- Changes some log output to use the FeatureBase name instead of the Pilosa name.
- Changes the default data directory from `~/.pilosa` to `/opt/molecula/featurebase`
- Changes the default node name from `pilosa0` to `featurebase0` <!-- TODO: is this correct? -->

Starting with FeatureBase 5.0, the `featurebase` versions of these will be used by default.

### Ingesters

Several configuration parameters will be renamed, replacing "pilosa" with "featurebase":

- `--pilosa-hosts` will become `--featurebase-hosts`
- `--pilosa-grpc-hosts` will become `--featurebase-grpc-hosts`
- `--assume-empty-pilosa` will become `--assume-empty-featurebase`

In Molecula version 4.4 (ingester version 0.22.0) and later, until the next major release (FeatureBase 5.0), the `featurebase` versions of the flags can be enabled by setting the boolean configuration parameter `--future.rename`. Starting with FeatureBase 5.0, the `featurebase` versions of these will be used by default.

### Deprecation plan

In Molecula version 4.4 (Pilosa version 3.4) and later, until the next major release (FeatureBase 5.0), the Pilosa name will be used by default, and FeatureBase can optionally be used by setting the `--future.rename` configuration flag.

In FeatureBase 5.x, the effects of the `--future.rename` flag will be applied by default, and will not be revertible. The `--future.rename` flag will still be present, and setting it will have no effect.
