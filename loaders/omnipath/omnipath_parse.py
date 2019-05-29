"""
Parses Omnipath data file, creates json
    :argument: DATA_FILE: http://omnipathdb.org/interactions/?fields=sources&fields=references
    :argument: EXPORT_FILE: output json location
"""
import os, json 

# Defining constants
DATA_FILE = 'omnipath_0.7.111.txt'
taxid = 9606
directory = 'omnipath_0.7.111/interactor_a_tax_id=%s' % (str(taxid))
EXPORT_FILE = directory + '/omnipath.json'

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
    source_id = line[0].strip()
    target_id = line[1].strip()
    
    # Pubmed id
    pmid = []
    for pub in line[7].split(';'):
        pmid.append(int(pub))
        
    # Int detection method
    detect = []
    
    # Int types
    int_type = []
    if line[2] == '1':
        int_type.append(407)

    elif line[3] == '1':
        int_type.append(624)

    elif line[4] == '1':
        int_type.append(623)
        
    else:
        int_type = []
    
    # Source DB
    sourcedb = []
    source_map = {
        'TRIP': None,
        'BioGRID': 463,
        'HPRD': 468,
        'IntAct': 469,
        'Signor': 2214,
        'PhosphoSite': None,
        'PhosphoSite_dir': None,
        'ELM': None,
        'phosphoELM': None,
        'LMPID': None,
        'SPIKE': 1115,
        'MIMP': None,
        'InnateDB': 974,
        'SignaLink3': 2270,
        'MPPI': None,
        'PDZBase': None,
        'PhosphoSite_noref': None,
        'CA1': None,
        'PhosphoNetworks': None,
        'KEGG': 470,
        'PhosphoPoint': None,
        'CancerCellMap': None,
        'DEPOD': None,
        'DIP': None,
        'HPRD-phos': 468,
        'ACSN': None,
        'Macrophage': None,
        'NRF2ome': None,
        'Li2012': None,
        'MatrixDB': 917,
        'Guide2Pharma': None,
        'ARN': None,
        'DeathDomain': None,
        'DOMINO': None,
        'Wang': None,
        'dbPTM': None,
        'Ramilowski2015': None,
        'HPMR': None,
        'CellPhoneDB': None,
        
        
    }
    for source in line[6].split(';'):
        if source_map[source] is not None:
            sourcedb.append(source_map[source])
                
    # For only human taxid interactions
    taxid = 9606
    # Adding values to output format
    one_int = {"interactor_a_id": source_id.lower(),"interactor_b_id": target_id.lower(), \
                   "interactor_a_id_type": "uniprotac", "interactor_b_id_type": "uniprotac","interactor_b_tax_id": taxid, \
                   "interactor_a_molecula_type_mi_id": 326,"interactor_b_molecula_type_mi_id": 326, \
                   "interactor_a_molecula_type_name": 'protein',"interactor_b_molecula_type_name": 'protein', \
                   "interaction_detection_methods_mi_id": detect,"interaction_types_mi_id": int_type, \
                   "source_databases_mi_id": sourcedb,"pmids":pmid}
        
    return one_int
    
def main():
    counter = 0
    # Parsing file
    with open(DATA_FILE) as data, open(EXPORT_FILE, 'w') as outjson:
        # Skipping the header
        data.readline()
        for line in data:
            # Adding 1000 line limit, uncomment following 4 lines for testing
            #counter += 1
            #if counter == 1000:
            #    break
            #else:
            line = line.split('\t')
            if len(line) > 1:
                    # Calling parsing function
                    one_int = get_data(line)
                    # Adding to output
                    json.dump(one_int, outjson)
                    outjson.write('\n')

                          
if __name__ == '__main__':
    print("Parsing database...")
    main()
    print('Parsing done!')
