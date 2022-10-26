## Source

/data-modeling-guide/_posts/2022-04-01-data-modeling.md

## Content (To be restructured)

<p class="warning">NOTE TO SELF: This content would be better presented as **actual** SQL query examples in the appropriate SQL/PQL pages</p>

In FeatureBase, you can model things as you typically would in a relational database with facts and dimensions split apart, but FeatureBase has some unique capabilities that give you more options. Usually when you're doing queries that involve facts, you're not interested in the events themselves, but one of the dimensions that they affect. For example, you might want to know how many users visited a certain blog post as opposed to how many times that blog post was visited. They sound similar, but the first query is typically much more difficult because you're counting the distinct number of users rather than the number of events. In FeatureBase, you could add a "pages_visited" set type field directly to your users dimension and get the distinct functionality essentially for free. The power of the set field is that it can track multiple pages visited per user without additional overhead.

But wait! There's more. What if you only wanted to get the set of users who visited a page within the past month? You'd have to go back to joining the facts with the dimension right? Nope. FeatureBase also has "time" fields which are just like set fields except you have the option to associate a coarse-grained timestamp with every user-page association (in fact you can have multiple timestamps associated with a single user-page pair). Currently the timestamps can be at yearly, monthly, daily, or hourly granularity, and FeatureBase lets you query across arbitrary time ranges.

It takes up more space to store things like this, but if you have a workload that demands low latency for these types of queries it can be a very worthwhile tradeoff over storing the facts separately and joining across the dimensions at query time.
