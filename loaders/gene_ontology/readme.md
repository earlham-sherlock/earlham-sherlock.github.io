# Gene Ontology Loader script


**Description:**

This script takes an OBO Gene Ontology (GO) file, which contains gene ontologies
and converts it to Sherlock compatible JSON format.

The working directory can be a non-existent folder as well!


**Parameters:**

-i, --input-file <path>         : path to an existing .obo file [mandatory]

-wd, --working-directory        : path to a folder, where the script can work in [mandatory]


**Exit codes**

Exit code 1: The specified input file does not exists!
Exit code 2: The specified input file is not an OBO file!


**Useful links**

Information about the relationship between ontology terms: http://geneontology.org/docs/ontology-relations/
