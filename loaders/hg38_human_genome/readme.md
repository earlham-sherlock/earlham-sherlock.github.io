# Hg38 Human Genome loader script


**Description:**

This script cuts up the input genome into regions with specified lenght. This script can provide an input fasta file or
several input fasta files, which contain(s) the whole genome of an organism. An output folder is also mandatory. With
the region length parameter, you can specify how long regions will be the genome divided.


**Parameters:**

-i, --input-files <comma separated list of fasta file paths> [mandatory]

-o, --output-folder <path to an output folder> [mandatory]

-l, --region-length <the value of the length of the cutting region> [mandatory]


**Exit codes**

Exit code 1: One of the specified input file doesn't exists!
Exit code 2: This is not a fasta file!
Exit code 3: The specified output folder doesn't exists!


**Useful links**

The whole genome per chromosomes (UCSC): http://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/
