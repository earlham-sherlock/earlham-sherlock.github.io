[BACK](./readme.md) to main page

# Backup and restore metadata

In Sherlock, almost all the data is kept in S3. This also means, that you can stop and start Presto any 
time, you won’t lose any data. But Presto is using the Metastore service to keep metadata about table 
and view structures. It means, that if you restart Sherlock, although you still have all the old data, 
but Presto will not remember where to find this data in S3, because the Metastore lost all the schema 
related info.

You can backup the state of the Metastore to S3, using the `metastore_backup.sh` command. You also have 
to specify a backup path as a parameter. It will create a backup file in the same S3 bucket you 
specified in your sherlock config file. Similarly, you can use the `metastore_restore.sh` command to 
restore a backup with a given name from S3 after you restarted the Sherlock cluster.

```
export SHERLOCK_CONF=`pwd`/conf/config-example_many_workers_external-s3.conf
 
./metastore_backup.sh sherlock_metastore_backups/backup_2019-05-22.dump
```

If you are opening now the `sherlock_metastore_backups` folder on an S3 browser (e.g. in case of using the local 
sandbox S3: http://localhost:9000/minio/sherlock/sherlock_metastore_backups/), then you can 
see the dump file generated:

![Sherlock metastore backups in S3](./images/minio_ui.png)


You can restore the backup later (e.g. after restarting the cluster), using the following command:

```
export SHERLOCK_CONF=`pwd`/conf/config-example_many_workers_external-s3.conf
 
./metastore_restore.sh sherlock_metastore_backups/backup_2019-05-22.dump
```

---
© 2018, 2019 Earlham Institute ([License](./license.md))