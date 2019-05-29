# Data lake structure and schema initialization in Sherlock


You can use Sherlock to execute queries on top of a Data Lake, where all the data is stored in 'folder-like' structures. 
Having well defined folder structure helps you to organize your data better.  Our suggestion 
is to separate your data in the Data Lake into four different main folders, representing different 
stages of your data and different access patterns in the Data Lake. We are calling these main folders as 'zones`.
Inside each of these main folders you can create subfolders, and it is a good practice to incorporate 
the name of the data set, the data owner name, the creation date (or other version info), and the file formats 
somehow into the paths.

![Main components of Sherlock](images/overview.svg)

The four main zones are built on top of each other.

Into the **RAW ZONE** you archive all the database files in their original formats. E.g. if you download the human 
genome, then you put the fasta files here, under a separate subfoler. The name of the subfolder should contains the 
exact version (e.g. hg38_p12), and also you should put a small readme file to the folder, where you list some metadata,
like the date and url of the download, etc. Usually you can not open these files with presto, as the file format is
incompatible in most of the cases.

You need to develop specific scripts, converting each of the raw datasets into the **LANDING ZONE**. We are suggesting 
to convert the data to a json text file, which can be opened by Presto. This is a specific json format, where each
line of the text file representing a single json record. You can put the json file(s) for each
dataset into a separate sub-folder in the landing zone, then register a table in Presto, pointing to the
new folder. Presto will be able to load the data, also you can execute simple data transformations on top of it. However, 
we don't recommend to use the tables in this zone for querying, as processing the large json files is very slow.
If you want, you can also use our converter scripts [here](https://github.com/NetBiol/sherlock/tree/master/loaders) 
to generate sherlock compatible json files.

Using Presto, you can convert the data from the landing zone into optimized (ordered, indexed, binary) format in the
**MASTER ZONE**. The main idea is, that you can use the tables in the master zone later for analytical queries. You 
can use advanced bucketing or partitioning on these tables to optimize your queries. The master zone contains the
'single source of truth'. The data here is not changed, only extended (e.g. adding new version of the datasets).

In the Project zone you are saving the tables which are needed only for some projects. you can even create multiple
project zones, one for each group / user. It is important to have a rule to indicate the owner of the tables here.
We are using a naming convention, to prefix the table name with the user who created the table and who is responsible
for it.

In [this page](loaders/load_interaction_data.md) you can see how can you load molecular interaction data to Sherlock.

---
© 2018, 2019 Earlham Institute ([License](license.md))