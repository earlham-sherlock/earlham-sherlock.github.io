"""
 Tissue expression data from:
https://bgee.org/?page=download&action=proc_values#id5
"""

# Imports
import os, json, io

# Defining constants
RNA_SEQ_LIST = []
AFF_LIST = []

taxid = '9606'
out_dir = 'bgee_14_0/tax_id=%s' % (taxid)
EXPORT_FILE = out_dir + '/bgee.json'

# Creating export directory if not exist
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Removing output file if exists
try:
    os.remove(EXPORT_FILE)
except OSError:
    pass

# Getting to-be-parsed file names, adding them to lists
for directory in os.listdir('bgee_files'):
    # Only searching through already unzipped directories
    if directory.endswith('.zip'):
        pass
    else:
        if 'RNA' in directory:
            for file in os.listdir('bgee_files/' + directory):
                if file.endswith('.tar'):
                    pass
                else:
                    # Adding filenames to lists
                    RNA_SEQ_LIST.append('bgee_files/' + directory + '/' + file)
        elif 'Affymetrix' in directory:
            for file in os.listdir('bgee_files/' + directory):
                if file.endswith('.tar'):
                    pass
                else:
                    # Adding filenames to lists
                    AFF_LIST.append('bgee_files/' + directory + '/' + file)


def get_RNA_data(RNA_line):
    """
      Gets data from human RNA-seq data file from Bgee,
      assigns variables and returns a line of the final json file.
       :param: RNA_line: one line from input file

    """

    # Assigning variables
    if len(RNA_line) > 4:
        gene_id = RNA_line[3].strip().lower()
        if ':' in RNA_line[4]:
            uberon_id = RNA_line[4].split(':')[1]
    else:
        uberon_id = None
    if len(RNA_line) > 11:
        tissue_name = RNA_line[5].replace('"', '')
        FPKM_score = float(RNA_line[11])
    else:
        tissue_name = None
        FPKM_score = None

    # Assembling one line
    # If species is not human, "molecule_id_type" will be different!!
    if uberon_id is not None:
        tissue = {"molecule_id": gene_id, "molecule_id_type": "ensembl", "tissue_uberon_id": int(uberon_id),
                  "tissue_uberon_name": tissue_name, "source_db": "bgee", "score": FPKM_score}

        return tissue


def get_chip_data(chip_line):
    """
      Gets data from human Affimetrix probeset data file from Bgee,
      assigns variables and returns a line of the final json file.
        :param: CHIP_line: one line from input file

    """

    # Assingning variables
    if len(chip_line) > 4:
        gene_id = chip_line[3].strip().lower()
        if ':' in chip_line[4]:
            uberon_id = chip_line[4].split(':')[1]
        else:
            uberon_id = None
        tissue_name = chip_line[5].replace('"', '')

        # Assembling one line
        # If species is not human, "molecule_id_type" will be different!!
        if uberon_id is not None:
            tissue = {"molecule_id": gene_id, "molecule_id_type": "Ensembl", "tissue_uberon_id": int(uberon_id),
                      "tissue_uberon_name": tissue_name, "source_db": "Bgee", }

            return tissue


def main(rna_filelist, aff_filelist):
    counter = 0
    # Opening output file for writing
    with open(EXPORT_FILE, 'w') as outjson:
        # For every collected file
        for rna_file, chip_file in zip(rna_filelist, aff_filelist):
            # Adding 2 file limit, uncomment following 4 lines for testing
            counter += 1
            if counter == 4:
                break
            else:
                # Opening data files for parsing
                with open(rna_file) as rnafile, open(chip_file) as chipfile:

                    # RNA-seq data
                    # Skipping header
                    rnafile.readline()
                    for rna_line in rnafile:
                        rnaline = rna_line.strip().split('\t')
                        # Calling parsing funtion on each line of file
                        one_json_line = get_RNA_data(rnaline)
                        # Adding line to output with line separator after each line
                        json.dump(one_json_line, outjson)
                        outjson.write('\n')

                    # Affimetrix data
                    # Skipping header
                    chipfile.readline()
                    for chip_line in chipfile:
                        chipline = chip_line.strip().split('\t')
                        # Calling parsing funtion on each line of file
                        one_json_line = get_chip_data(chipline)
                        # Adding line to output with line separator after each line
                        json.dump(one_json_line, outjson)
                        outjson.write('\n')


if __name__ == '__main__':
    print("Parsing database...")
    main(RNA_SEQ_LIST, AFF_LIST)
    print('Parsing done!')


