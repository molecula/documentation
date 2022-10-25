## Issue

FeatureBase Community won't startup on Mac OS after successful installation.

## Probable cause

This may be caused by the MacOS Gatekeeper system
* [Learn about Apple Mac Gatekeeper and the Quarantine flag](https://support.apple.com/en-gb/HT202491 )

## Solution

1. Open a Terminal Window
2. Execute the following command to deactivate the Quarantine flag

```
mv featurebase-*-community-darwin-arm64/ opt
mv idk-*-arm64 idk
```

## Further information

If these steps don't work, you can try reinstalling the software.

* [How do I install FeatureBase Community locally?](/community/part1-install-fb-locally.md)
