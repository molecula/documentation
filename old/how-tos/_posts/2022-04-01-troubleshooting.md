---
id: troubleshooting
title: Troubleshooting FeatureBase
sidebar_label: Troubleshooting FeatureBase
---

## FeatureBase Stops Or Won't Start

Check the logs. Depending on how you're running FeatureBase, this can take a few different forms. 

If you're running directly from the command line, you should see some output at the command line. If you don't see anything useful, take a look at your configuration (check the command line flags, environment variables, and config file if applicable). See if you have a log path specified, and if so, go check there to see the FeatureBase logs.

If you're running under systemd, you should certainly check any configured log file as above, but you can also check to see what FeatureBase is saying on stdout or stderr by running the command `journalctl -u featurebase -f`. The `-f` option works similarly to the `tail` command and you can leave it off if you want to see the full log from the beginning of time.

If there isn't a clear error in any of the logs, next you'll want to check your kernel logs. This is a little bit OS dependent, but usually you can do something like `tail -f /var/log/syslog` or `dmesg | tail`. The most common thing to see here would be something like `OOM Killed` or `Out of memory: Kill process 764` which indicates that FeatureBase is being terminated by the OS without warning for using too much memory.


## FeatureBase throws an error like "cannot allocate memory"

This can happen a few different ways, but typically indicates that the mmap syscall is returning ENOMEM. Confusingly it usually doesn't mean that you're actually out of memory. Most often it means that you either:

1. Have surpassed the system limit for maximum mmap count. You can try `sysctl vm.max_map_count` to read this value. Default is typically something like 65530, and you might want to set it higher... to something like 256000. You can do this adding a line like `vm.max_map_count=256000` to `/etc/sysctl.conf` and then applying the setting with `sysctl -p`. Or setting it temporarily with `sysctl -w vm.max_map_count=256000`. In either case, you will need to restart FeatureBase after making these changes

2. You're actually out of memory address space. This can happen because the RBF storage backend maps 4GB memory regions per file by default, and if you get up near 16000 files, you can actually exhaust the address space. In this case, you can tune FeatureBase's RBF settings to reserve less space for each RBF file:

```
[rbf]
max-db-size = 1073741824
max-wal-size = 1073741824
```

In this example we've tuned the RBF DB and WAL files to have a maximum size of 1GiB instead of 4GiB. The drawback here is that the maximum size of a shard is now more restricted. Take a look at your existing data directory before you do this and make sure that you don't have any shard files near the limit you're setting. You can find shard files in your data directory under `indexes/<indexname>/backends/rbf/shard.XXXX`. If you find yourself in a situation where you can't tune this down because you have large shards, but you need to because you're running into this error, please let the customer success team know. You may need to add more nodes to your cluster, or our engineering team might want to look at other possible solutions.
