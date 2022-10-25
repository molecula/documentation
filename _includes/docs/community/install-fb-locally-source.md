Featurebase Community edition is free to install for [N users | Other limits | No limits]

## Before you begin

FeatureBase Community can be installed on the following operating systems:
* Mac OSX
* Linux
* Windows (running Linux, see below)

System requirements:
* Application: nnGB RAM
* Install footprint: nnGB on HD
* Data: nnGB on HD

Software requirements:
* Windows installations:
  * Windows Linux Subsystem running Ubuntu 20, OR
  * Linux in a Virtual Machine
* Install Git

Other requirements:
* Administrator privileges
* Github account
* Create Featurebase directory for install files

## How do I install FeatureBase community

NOTE: Windows users: These instructions can be performed in the Windows Linux Subsystem or a Linux Virtual Machine

### Step 1: Download FeatureBase

[Download Featurebase from the Community repository in Github](https://github.com/FeatureBaseDB/FeatureBase/releases)

### Step 2: Untar the install files to the Featurebase directory

1. Open a terminal window
2. Enter the following command, substituting your FeatureBase directory:

```
# tar xvfz featurebase-*-arm64.tar.gz -C /target/directory
```

### Step 3: Move the directories

* Enter the following commands to move the folders to the correct directory:

```
mv featurebase-*-community-darwin-arm64/ opt
mv idk-*-arm64 idk
```

## Next step

* Start Featurebase Community Edition

## Further information

* Additional useful info
