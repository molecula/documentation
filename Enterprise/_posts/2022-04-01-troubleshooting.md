---
id: troubleshooting
title: Troubleshooting and Support
sidebar_label: Troubleshooting and Support
---

## Support Channels

*   Please contact FeatureBase Support at [support@featurebase.com](mailto:support@featurebase.com) for help!
*   We're happy to share a Slack channel, and are available for in-person meetings and calls as needed.


## Things to Have Handy

*   Logs
*   Metrics
*   Host Metrics (memory, disk)
*   Traces

It may be necessary to restart FeatureBase with verbose logging or more granular tracing enabled.


## Profiling

If you are experiencing performance issues, we'll likely ask you to profile various components. All components written in Golang have profiling support enabled, this is described in detail here: [https://golang.org/pkg/net/http/pprof/](https://golang.org/pkg/net/http/pprof/). As a quick reference example:


```shell
wget host:port/debug/pprof/profile?seconds=10
```


which will download a file that you can send over for analysis, or


```shell
go tool pprof host:port/debug/pprof/profile?seconds=10
```


which will directly bring up Go's command line tool for viewing and analyzing profiling information.
