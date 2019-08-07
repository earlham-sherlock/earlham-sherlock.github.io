# Uberon Ontology Loader script


**Description:**

This script takes an OBO Uberon Ontology (GO) file, which contains ontologies
and converts it to Sherlock compatible JSON format.

The working directory can be a non-existent folder as well!


**Parameters:**

-i, --input-file <path>         : path to an existing .obo file [mandatory]

-wd, --working-directory <path> : path to a folder, where the script can work in [mandatory]


**Exit codes**

Exit code 1: The specified input file does not exists!
Exit code 2: The specified input file is not an OBO file!
