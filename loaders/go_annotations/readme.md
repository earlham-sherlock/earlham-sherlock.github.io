# GO Annotations Loader script


**Description:**

This script takes a GAF GO Annotation file, which contains annotations
and converts it to Sherlock compatible JSON format.

We keep only the following information from the GAF file:
- column1: DB
- column2: DB Object ID
- column5: GO ID
- column7: Evidence Code


**Parameters:**

-i, --input-file <path>         : path to an existing .gaf file [mandatory]

-t, --tax-id <int>              : taxonomy identifier [mandatory]


**Exit codes**

Exit code 1: The specified input file does not exists!
Exit code 2: The specified input file is not a GAF file!
