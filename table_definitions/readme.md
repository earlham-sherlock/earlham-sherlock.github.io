# Refreshing partition list

When you register a new table with multiple partitions in the Hive Metastore, it will be initially
registered without any actual partitions. You can do this in the hive client, or you can also do
it using hive CLI on the metastore docker image.

Execute this command in the hive CLI to refresh the partitions for table `landing.test`:
```
"msck repair table landing.test;"
```

When you create a table using the `create table as ...` SQL command in presto, then you don't need
to refresh the partition list, presto and hive will do that automatically. But you need to do it if
you register a new external table.