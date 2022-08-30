---
id: set-up-log-rotation
title: How To Set Up Log Rotation
sidebar_label: Set Up Log Rotation
---



When logging to a file, FeatureBase components will re-open the log file on receipt of the HUP signal. This allows for seamless log rotation. As an example, to configure log rotation with FeatureBase:

1. First create a log directory owned by the system user that runs the FeatureBase process; we recommend `/var/log/molecula`.

2. Next, configure FeatureBase to write to a file in that new directory. Edit your featurebase.conf and add `log-path = "/var/log/molecula/featurebase.log"`.

3. Restart FeatureBase for the new logging configuration to take effect.

4. Ensure that [logrotate](https://linux.die.net/man/8/logrotate) is installed and configured to run daily with cron. This should be the default after installation on most Linux systems. Check `/etc/cron.daily/logrotate` to make sure.

5. Add a new logrotate configuration file at `/etc/logrotate.d/featurebase` with the following contents:

```text
/var/log/molecula/featurebase.log {
    missingok
    notifempty
    rotate 7
    daily
    compress
    postrotate
        pkill -HUP featurebase
    endscript
}
```

6. Repeat steps 2-5 for the Ingesters, replacing references to FeatureBase where appropriate.

Note that `pkill -HUP featurebase` may not be reliable and that you should use `kill -HUP $(cat /path/to/pidfile)` if you are using a PID file.
