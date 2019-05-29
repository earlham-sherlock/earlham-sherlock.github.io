
### Fetching a sequence region around an SNP

In this example, we have a single point mutation on chromosome 11, in position 58723, and we 
wish to fetch the wild type sequence around this SNP, let's say in +/- 700 length.

The following query also expects that we store the sequence in at least 700 long chunks in the 
data lake (what we do actually). The inner query part will fetch 3 chunks from the genome,
and the outer part will split our region of interest from this "large sequence". The query 
also handles the case, when there is no 700 long sequence around the SNP (e.g. if the mutation
is positioned int he very beginning or very end of the chromosome).


```$sql
SELECT 
   SUBSTR(long_sequence, 
          MAX(1, SNP_POS-700-long_sequence_start), 
          MIN(LENGTH(long_sequence) - (MAX(1, SNP_POS-700-long_sequence_start)), SNP_POS+700-long_sequence_start) ) 
   AS result
FROM (
        SELECT 
            ARRAY_JOIN ( ARRAY_AGG(genome.sequence ORDER BY genome.start) ) AS long_sequence
            MIN(genome.start) AS long_sequence_start
        FROM master.hg38 genome
        WHERE genome.chr = ‘chr11’
          AND genome.start BETWEEN SNP_POS - 2000 AND SNP_POS + 1000;
      );
```

---
© 2018, 2019 Earlham Institute ([License](../license.md))
