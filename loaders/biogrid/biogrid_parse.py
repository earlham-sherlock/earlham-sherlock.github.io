"""
Parses biogrid data file, creates json
    :argument: DATA_FILE: https://downloads.thebiogrid.org/Download/BioGRID/Release-Archive/BIOGRID-3.5.169/BIOGRID-SYSTEM-3.5.169.mitab.zip
    :argument: EXPORT_FILE: output json location
"""
import os, json

# Defining constants
DATA_FILE = 'BIOGRID-ALL-3.5.169.mitab.txt'
taxid = 9606
directory = 'biogrid_3.5.169/interactor_a_tax_id=%s' % (str(taxid))
EXPORT_FILE = directory + '/biogrid.json'

# Creating export directory if not exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Removing output file if exists
try:
    os.remove(EXPORT_FILE)
except OSError:
    pass


def get_data(line):
    # Setting variables for easier use
    source_id = line[0].strip().split(':')[1]
    target_id = line[1].strip().split(':')[1]
    # Pubmed id
    pmid = []
    for pub in line[8].split('|'):
        if 'pubmed' in pub:
            try:
                if int(pub.split(':')[1]) not in pmid:
                    pmid.append(int(pub.split(':')[1]))
            except ValueError:
                pass
        else:
            pass
    # Int detection method
    detect = []
    for det in line[6].split('|'):
        miid_full = det.split('"')[1]
        miid = miid_full.split(':')[1]
        if int(miid) not in detect:
            detect.append(int(miid))
    # Int types
    int_type = []
    for inttype in line[11].split('|'):
        miid_full = inttype.split('"')[1]
        miid = miid_full.split(':')[1]
        if int(miid) not in int_type:
            int_type.append(int(miid))
    # Source DB
    sourcedb = []
    source = line[12].strip()
    miid_full = source.split('"')[1]
    miid = miid_full.split(':')[1]
    sourcedb.append(int(miid))

    # Screening for only human taxid interactions
    if line[9] == 'taxid:9606' and line[10] == 'taxid:9606':
        taxid = 9606
        # Adding values to output format
        one_int = {"interactor_a_id": source_id.lower(),
                   "interactor_b_id": target_id.lower(),
                   "interactor_a_id_type": "entrez gene",
                   "interactor_b_id_type": "entrez gene",
                   "interactor_b_tax_id": taxid,
                   "interactor_a_molecula_type_mi_id": 250,
                   "interactor_b_molecula_type_mi_id": 250,
                   "interactor_a_molecula_type_name": 'gene',
                   "interactor_b_molecula_type_name": 'gene',
                   "interaction_detection_methods_mi_id": detect,
                   "interaction_types_mi_id": int_type,
                   "source_databases_mi_id": sourcedb,
                   "pmids": pmid}

        return one_int

    else:
        return 'Not human'


def main():
    counter = 0
    # Parsing file
    with open(DATA_FILE) as data, open(EXPORT_FILE, 'w') as outjson:
        # Skipping the header
        data.readline()
        for line in data:
            # Adding 1000 line limit for testing
            counter += 1
            if counter == 1000:
                break
            else:
                line = line.split('\t')
                if len(line) > 1:
                    # Calling parsing function
                    one_int = get_data(line)
                    # Only using human data, change if neccesary
                    if one_int != 'Not human':
                        # Adding to output
                        json.dump(one_int, outjson)
                        outjson.write('\n')


if __name__ == '__main__':
    print("Parsing database...")
    main()
    print('Parsing done!')

