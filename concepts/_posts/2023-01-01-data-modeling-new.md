
Need to gather high level information on the databases here.

Source: /community/community-database/size-featurebase-database

FeatureBase breaks data into shards which are, by default, 2^20 (1,048,576) records. It is useful to figure out approximately how large each of your shards will be, and then use that to extrapolate memory requirements. The most accurate way to do this is to load a shard's worth of data into FeatureBase and measure its size on disk. Below is a table of some typical field configurations, and how much space they use, as a starting point for estimating hardware sizes. Please keep in mind that depending on data distribution, the actual size in your case might vary significantly from these numbers.
