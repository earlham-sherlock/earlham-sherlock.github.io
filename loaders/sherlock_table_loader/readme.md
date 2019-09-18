# Sherlock Table Loader script


**Description:**

This script takes a TSV/CSV file, which contains any type of data
and converts it to Sherlock compatible JSON format.<br>
Then it uploads the json file to the landing zone on S3, registers it
into HIVE, uploads to the project zone in ORC format and deletes
it from the landing zone.


**Parameters:**

-i, --input-file-list <path>          : path to an existing TSV/CSV/MITAB file [mandatory]

-t, --table-name <str>                : name of the table what you want to upload to sherlock [mandatory]

-o, --output-file <path>              : path to an output json file [mandatory]


**Requirements for the input file:**

1) The input file must be a tab separated file!
2) The first line should contain the names of the columns in the table!
3) The second line should contain the type of data in the columns of the table! Available types:
    - for STRING (text): the second line should be 'varchar' (see in the example input file)
    - for INTEGER (numbers): the second line should be 'int'
    - for FLOAT (float numbers): the second line should be 'double'


**Exit codes**

Exit code 1: The specified input file does not exists!
Exit code 2: One of the column name has a special character!
Exit code 3: One of the column type is incorrect!


**Example:**

Input example file (example_files/test.tsv)
```
uidA	uidB	altA	altB
varchar	varchar	[]varchar	[]varchar
rogid:Of52wNDoUXUvgK63WvExugES/OY4932	uniprotkb:P22213	pdb:1MQS,pdb:1MQS_A,rogid:Of52wNDoUXUvgK63WvExugES/OY4932,irogid:9981421	cygd:YDR189W,entrezgene/locuslink:851770,refseq:NP_010475,rogid:wymTcFMVeTdrOMFsga2RxUW7l30559292,irogid:16830363
refseq:NP_009441	uniprotkb:P23291	refseq:NP_009441,rogid:XW6crPzeZEXaIm7/d/sFOYULWnE4932,irogid:4935553	cygd:YHR135C,entrezgene/locuslink:856537,refseq:NP_012003,rogid:pFpwRNbvvNZ1NPc7VMVXSivwMeI559292,irogid:16822056
uniprotkb:A0A024RB10	rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932	entrezgene/locuslink:1017,refseq:NP_439892,uniprotkb:A0A024RB10,rogid:oTPS6iaQr9AvqaEhdsxHbF1VaIQ9606,irogid:3437630	pdb:1US7,pdb:1US7_A,rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932,irogid:53113770
uniprotkb:P0CI39	uniprotkb:P11972	uniprotkb:P06842,uniprotkb:P0CI39,rogid:Xw+4tatIKPl42hhE5XQUighaCP44932,irogid:4934910	cygd:YLR452C,entrezgene/locuslink:851173,refseq:NP_013557,rogid:a452jzptv3MtejNfc+LDrwSFSks559292,irogid:16830889
uniprotkb:A0A024RB10	rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932	entrezgene/locuslink:1017,refseq:NP_439892,uniprotkb:A0A024RB10,rogid:oTPS6iaQr9AvqaEhdsxHbF1VaIQ9606,irogid:3437630	pdb:1US7,pdb:1US7_A,rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932,irogid:53113770
```

Terminal command:
`python3 sherlock_table_loader.py -i example_files/test.tsv -t test -o example_files/output.json`

The output will be (example_files/output.json)
```
{"uidA": "rogid:Of52wNDoUXUvgK63WvExugES/OY4932", "uidB": "uniprotkb:P22213", "altA": ["pdb:1MQS", "pdb:1MQS_A", "rogid:Of52wNDoUXUvgK63WvExugES/OY4932", "irogid:9981421"], "altB": ["cygd:YDR189W", "entrezgene/locuslink:851770", "refseq:NP_010475", "rogid:wymTcFMVeTdrOMFsga2RxUW7l30559292", "irogid:16830363"]}
{"uidA": "refseq:NP_009441", "uidB": "uniprotkb:P23291", "altA": ["refseq:NP_009441", "rogid:XW6crPzeZEXaIm7/d/sFOYULWnE4932", "irogid:4935553"], "altB": ["cygd:YHR135C", "entrezgene/locuslink:856537", "refseq:NP_012003", "rogid:pFpwRNbvvNZ1NPc7VMVXSivwMeI559292", "irogid:16822056"]}
{"uidA": "uniprotkb:A0A024RB10", "uidB": "rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932", "altA": ["entrezgene/locuslink:1017", "refseq:NP_439892", "uniprotkb:A0A024RB10", "rogid:oTPS6iaQr9AvqaEhdsxHbF1VaIQ9606", "irogid:3437630"], "altB": ["pdb:1US7", "pdb:1US7_A", "rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932", "irogid:53113770"]}
{"uidA": "uniprotkb:P0CI39", "uidB": "uniprotkb:P11972", "altA": ["uniprotkb:P06842", "uniprotkb:P0CI39", "rogid:Xw+4tatIKPl42hhE5XQUighaCP44932", "irogid:4934910"], "altB": ["cygd:YLR452C", "entrezgene/locuslink:851173", "refseq:NP_013557", "rogid:a452jzptv3MtejNfc+LDrwSFSks559292", "irogid:16830889"]}
{"uidA": "uniprotkb:A0A024RB10", "uidB": "rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932", "altA": ["entrezgene/locuslink:1017", "refseq:NP_439892", "uniprotkb:A0A024RB10", "rogid:oTPS6iaQr9AvqaEhdsxHbF1VaIQ9606", "irogid:3437630"], "altB": ["pdb:1US7", "pdb:1US7_A", "rogid:yyzsG0FP03JnFogf60kKLKG0bKo4932", "irogid:53113770"]}
```

In that example the table name in the landing and in the project zone will be 'test'!