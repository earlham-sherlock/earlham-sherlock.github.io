# SNP Database Loader script

**Description:**

This script takes a VCF file from SNP database, which contains SNPs
and converts it to Sherlock compatible JSON format.


**Parameters:**

-i, --input-file <path>                                       : path to an existing VCF SNP db file [mandatory]

-o, --output-folder <path>                                    : path to an output folder [optional]


**Exit codes**

Exit code 1: The specified input file does not exists!
Exit code 2: The specified input file is not a VCF file!
Exit code 3: The specified output folder does not exists!


**Notes**

1) The script keep only the following informations of SNPs:
- chromosome
- location
- snp identifier
- reference base(s)
- alt base(s)


**Example**

Input example file
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	10177	rs367896724	A	AC	.	.	RS=367896724;RSPOS=10177;dbSNPBuildID=138;SSR=0;SAO=0;VP=0x050000020005170026000200;GENEINFO=DDX11L1:100287102;WGT=1;VC=DIV;R5;ASP;VLD;G5A;G5;KGPhase3;CAF=0.5747,0.4253;COMMON=1;TOPMED=0.76728147298674821,0.23271852701325178
1	10352	rs555500075	T	TA	.	.	RS=555500075;RSPOS=10352;dbSNPBuildID=142;SSR=0;SAO=0;VP=0x050000020005170026000200;GENEINFO=DDX11L1:100287102;WGT=1;VC=DIV;R5;ASP;VLD;G5A;G5;KGPhase3;CAF=0.5625,0.4375;COMMON=1;TOPMED=0.86356396534148827,0.13643603465851172
1	10616	rs376342519	CCGCCGTTGCAAAGGCGCGCCG	C	.	.	RS=376342519;RSPOS=10617;dbSNPBuildID=142;SSR=0;SAO=0;VP=0x050000020005040026000200;GENEINFO=DDX11L1:100287102;WGT=1;VC=DIV;R5;ASP;VLD;KGPhase3;CAF=0.006989,0.993;COMMON=1
```

Terminal command:
`python3 snp_db_loader.py -i example_files/test.vcf -o example_files/dbsnp/`

The output will be:
- output file: chr=chr1/dbsnp.json
```
{"location": 10177, "snp_id": "rs367896724", "reference": "A", "alt": "AC"}
{"location": 10352, "snp_id": "rs555500075", "reference": "T", "alt": "TA"}
{"location": 10616, "snp_id": "rs376342519", "reference": "CCGCCGTTGCAAAGGCGCGCCG", "alt": "C"}
```
