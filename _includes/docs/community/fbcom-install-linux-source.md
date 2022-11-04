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

## Set the execute flag on `idk` executables

{% include /docs/community/fbcom-issue-permission-denied-ingest-source.md %}
