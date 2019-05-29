"""
Parses IntAct data file, creates json
    :argument: DATA_FILE:
ftp://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/intact-micluster.txt
    :argument: EXPORT_FILE: output json location
"""
import os, json

# Defining constants
DATA_FILE = 'intact_2018_11_02.txt'
taxid = 9606
directory = 'intact_2018_11_02/interactor_a_tax_id=%s' % (str(taxid))
EXPORT_FILE = directory + '/intact.json'

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
    if ':' in line[2] and line[2].split(':')[0] == 'uniprotkb':
        source_id = line[2].strip().split(':')[1]
    else:
        source_id = 'none'
    if ':' in line[3] and line[3].split(':')[0] == 'uniprotkb':
        target_id = line[3].strip().split(':')[1]
    else:
        target_id = 'none'
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
    for source in line[12].split('|'):
        miid_full = source.split('"')[1]
        miid = miid_full.split(':')[1]
        if int(miid) not in sourcedb:
            sourcedb.append(int(miid))

    # Screening for only human taxid interactions
    if line[9] == 'taxid:9606(human)' and line[10] == \
            'taxid:9606(human)':
        taxid = 9606
        # Adding values to output format
        one_int = {"interactor_a_id": source_id.lower(),
                   "interactor_b_id": target_id.lower(),
                   "interactor_a_id_type": "uniprotac",
                   "interactor_b_id_type": "uniprotac",
                   "interactor_b_tax_id": taxid,
                   "interactor_a_molecula_type_mi_id": 326,
                   "interactor_b_molecula_type_mi_id": 326,
                   "interactor_a_molecula_type_name": 'protein',
                   "interactor_b_molecula_type_name": 'protein',
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
            # counter += 1
            # if counter == 1000:
            #    break
            # else:
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

