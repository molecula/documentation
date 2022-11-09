---
id: hostsystem
title: Host System
sidebar_label: Host System
---

## Operating System Configuration

This page discusses software configuration issues commonly encountered when deploying FeatureBase. For hardware requirements or scaling, look at [Sizing FeatureBase](/concepts/size-featurebase-database).

FeatureBase's data storage splits the database into a potentially large number of files, which are open simultaneously. Most Unix-derived systems limit the number of simultaneous open files for a given process or user, and these limits are frequently small enough to be a problem. Similarly, there may be limits on the number of memory-mapped regions allowed in a process. These may need to be changed,
either temporarily during initial development and testing, or as a machine-wide configuration change that persists across restarts.

Throughout these instructions, commands given with a root prompt (`#`) are expected to require root privileges; you can run them in a root shell, or using `sudo`.

### Linux Systems

You can make temporary changes just to run the software once, or persistent changes which will survive reboots. We document both because the one-off changes are much easier to make, but in a production environment you will be happier making persistent changes.

To temporarily increase the open file limit, you should be able to use `ulimit -n`. If you can't set the limit high enough, you will need root privileges. The `ulimit` program only affects the limits of the shell it's run in and child processes of that shell, so you can't use `sudo ulimit` to change the limit of your current shell; if you need to set a higher limit, launch a new shell using `sudo -s` or the equivalent, then change the ulimit, then use `su` to start a new shell running as your regular user but inheriting the higher limits. We do not recommend running FeatureBase with root privileges.

To temporarily increase the allowable memory-mapped regions on a Linux system, you can use the `sysctl` command, or just the `proc` filesystem:

```shell
# sysctl -w vm.max_map_count=N
# echo N > /proc/sys/vm/max_map_count
```

#### Persistent Changes

There are two likely paths to setting the system open files limit on Linux systems. One is to look at `/etc/security/limits.conf`, or `/etc/security/limits.d/*.conf`, which allow you to specify the `hard` limit for the item `nofile` for any user or group. The other is to use `sysctl`, and change the `fs.file-max` variable. This can be changed through `/etc/sysctl.conf` or `/etc/sysctl.d/*.conf`. You can also use the `sysctl.conf` approach to change `vm.max_map_count` persistently.

Either way, you will need to restart your login session for the change to take effect, but it should be persistent after that. We recommend an open file limit of around 256K by default.

#### Enable noatime

Due to frequent access, using `atime` updates can significantly reduce the performance
of FeatureBase. `noatime` should be used on the mount point for the FeatureBase data directory.

```
  #!/bin/bash

  DATA_DIR="/opt/molecula/featurebase"

  PARTITION=$(df $DATA_DIR | awk 'NR==2 { print $1; exit }')

  MOUNT_POINT=$(df $DATA_DIR | awk 'NR==2 { print $6; exit }')

  MOUNT_OPTIONS=$(findmnt --source $PARTITION --output=options | sed -n '2p')

  if [[ "$MOUNT_OPTIONS" == *noatime* ]]; then
      echo "noatime is already enabled!"
  elif [[ $(lsblk $PARTITION -n --output=FSTYPE) == "xfs" && "$MOUNT_OPTIONS" == *relatime* ]]; then
      echo "reltime is enabled, mount with noatime to improve performance; to mount with noatime:"
      echo "    mount -o remount,noatime $PARTITION $MOUNT_POINT"
  else
      echo "noatime should be enabled on the mount point for the data directory; to mount with noatime:"
      echo "    mount -o remount,noatime $PARTITION $MOUNT_POINT"
  fi

```

#### Enable TRIM on SSDs

On SSDs, TRIM should be enabled to reclaim the memory blocks that are no longer considered to be 'in use'.

```
  #!/bin/bash

  DATA_DIR="/opt/molecula/featurebase"

  PARTITION=$(df $DATA_DIR | awk '{print $1}' | sed -n '2p')

  MOUNT_OPTIONS=$(findmnt --source $PARTITION --output=options | sed -n '2p')

  if [[ $(lsblk $PARTITION -n -o ROTA) == "1" ]]; then
      echo "The partition is on a rotational drive, TRIM not supported"
  elif [[ $(lsblk $PARTITION -n -o DISC-GRAN == "0B") ]]; then
      echo "DISC granularity 0, TRIM not supported"
  elif [[ $(systemctl is-enabled fstrim.timer) == "enabled" ]]; then
      echo "fstrim is already enabled!"
  else
      echo "fstrim must be enabled; to enable:"
      echo "    sudo systemctl enable fstrim.timer"
  fi

  if [[ "$MOUNT_OPTIONS" == *discard* ]]; then
      echo "Continuous TRIM(discard) is not recommended, switch to periodic TRIM(fstrim)"
  fi
 ```

### Mac OS Systems

On Mac OS, `ulimit` does not behave predictably, and the way to change the limits changes between releases. Additionally, the system's system integrity protection (SIP) functionality may prevent attempts to change this. For a more detailed writeup, have a look at Wilson Mar's [maximum limits](https://wilsonmar.github.io/maximum-limits/) page. The number of processes limit described there shouldn't be significant for FeatureBase. Mac OS does not seem to have a direct parallel to the maximum map count limits found on Linux systems.

You can temporarily raise the open file limit using `launchctl limit maxfiles 262144 262144`, although this will not persist across reboots. To persist it across reboots, you need to cause this command to be run during system startup every time. The easiest way to do this is by adding things to `/Library/LaunchDaemons`, but you can't do this while SIP is enabled, and you can't run `csrutil` once the system is up and running.

To disable the system integrity protection feature, restart your laptop, and hold down command + R to enter Recovery Mode. Open a terminal and enter `csrutil disable`, then restart your computer as you normally would. Now that SIP is disabled, you can create new LaunchDaemons files that will affect system limits. Copy the contents of this example plist file ([source](https://github.com/wilsonmar/mac-setup/blob/master/configs/limit.maxfiles.plist%20)) into a new file on your system located at `/Library/LaunchDaemons/limit.maxfiles.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>limit.maxfiles</string>
    <key>ProgramArguments</key>
    <array>
      <string>launchctl</string>
      <string>limit</string>
      <string>maxfiles</string>
      <string>262144</string>
      <string>262144</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>ServiceIPC</key>
    <false/>
  </dict>
</plist>
```

Once this file is created, change its ownership to `root:wheel` and tell `launchd` to load it:

```shell
# chown root:wheel /Library/LaunchDaemons/limit.maxfiles.plist
# launchctl load -w /Library/LaunchDaemons/limit.maxfiles.plist
```

As soon as the `launchctl limit` command runs (which also happens when you load the plist file), the limit is changed even in existing shells. To ensure the open file limit has successfully changed, run `ulimit -a`. Your open files should be set to a number greater than 256 (in the range of 262144). Once you're confident that the changes haven't destroyed anything, you probably want to turn SIP back on; go back to recovery mode, and run `csrutil enable`. You need the SIP functionality disabled to make these changes, but not to keep them once they've been made.

You may also need to adjust kernel parameters using `sysctl`, such as `kern.maxfiles` or `kern.maxfilesperproc`.

#### Enable noatime

Due to frequent access, using `atime` updates can significantly reduce the performance
of FeatureBase. `noatime` should be used on the mount point for the FeatureBase data directory.

```
  #!/bin/bash

  DATA_DIR="/opt/molecula/featurebase"

  PARTITION=$(df $DATA_DIR | awk 'NR==2 { print $1; exit }')

  MOUNT_POINT=$(df $DATA_DIR | awk 'NR==2 { print $9; exit }')

  MOUNT_OPTIONS=$(mount | grep -w $PARTITION)

  if [[ "$MOUNT_OPTIONS" == *noatime* ]]; then
      echo "noatime is already enabled"
  else
      echo "noatime should be enabled for the best performance; to mount with noatime:"
      echo "    mount -vuwo noatime $MOUNT_POINT"
  fi
```

#### Enable TRIM on SSDs

On SSDs, enable trim to reclaim the blocks of data are no longer considered to be 'in use'.
On APFS, Trim is enabled by default and macOS automatically performs a TRIM operation on the
free disk space on boot. Use `#trimforce enable` to ensure that the TRIM is enabled. 

### FeatureBase Trial Version
If you are using a trial version of FeatureBase ensure that the host (and by extension FeatureBase)
can access the ntp server `0.beevik-ntp.pool.ntp.org` via the UDP port 123.
