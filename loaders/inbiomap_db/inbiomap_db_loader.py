import argparse
import sys
import os
import json
from time import strftime


def parse_args(args):
    help_text = \
        """
        === InBioMap Database Loader script ===
        
        **Description:**
        
        This script takes an InBioMap database file, which contains protein-protein
        interactions and converts it to Sherlock compatible JSON format.
        
        The downloaded database file does not contain some of the parameters below!
        Because of this, the user have to identify these parameters!
        
        
        **Parameters:**
        
        -i, --input-file <path>                                       : path to an existing HINT db file [mandatory]
        
        -int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A [mandatory]
        
        -int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B [mandatory]
        
        -int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]
        
        -int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A [mandatory]
        
        -int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A [mandatory]
        
        -int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B [mandatory]
        
        -int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B [mandatory]
        
        -int_det_m, --interaction-detection-method <int>              : comma separated list of the detection methods of the interaction [optional]
        
        -int_type_id, --interaction-type-mi-id <int>                  : comma separated list of MI IDs of the interaction type [optional]
        
        -db, --source-db-mi-id <int>                                  : comma separated list of MI IDs of the database sources [optional]
        
        -pmid, --pubmed-id <int>                                      : comma separated list of pubmed IDs of the paper [optional]
        
        
        **Exit codes**
        
        Exit code 1: The specified input file doesn't exists!
        
        
        **Notes**
        
        1) The HINT database does not include the mi identifiers of the interaction types!
        2) HINT database does not have any Uniprot Ref identifier, that is why, we give an unique id for it, 10002!
        3) The interaction type is not in the database file, so we defined it according to the published paper of the database!
        It was 0915, physical association!
        4) The pubmed ID of the published paper for the HINT database is 27892958!
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-file",
                        help="<path to an existing HINT db file> [mandatory]",
                        type=str,
                        dest="input_file",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_id", "--interactor-a-id-type",
                        help="<ID type of interactor A> [mandatory]",
                        type=str,
                        dest="interactor_a_id_type",
                        action="store",
                        required=True)

    parser.add_argument("-int_b_id", "--interactor-b-id-type",
                        help="<ID type of interactor B> [mandatory]",
                        type=str,
                        dest="interactor_b_id_type",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_tax_id", "--interactor-a-tax-id",
                        help="<taxonomy ID of interactor A> [mandatory]",
                        type=int,
                        dest="interactor_a_tax_id",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_m_id", "--interactor-a-molecule-type-mi-id",
                        help="<MI ID entity type of interactor A> [mandatory]",
                        type=int,
                        dest="interactor_a_molecule_type_mi_id",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_m_tn", "--interactor-a-molecule-type-mi-term-name",
                        help="<MI term name entity type of interactor A> [mandatory]",
                        type=str,
                        dest="interactor_a_molecule_type_mi_term_name",
                        action="store",
                        required=True)

    parser.add_argument("-int_b_m_id", "--interactor-b-molecule-type-mi-id",
                        help="<MI ID entity type of interactor B> [mandatory]",
                        type=int,
                        dest="interactor_b_molecule_type_mi_id",
                        action="store",
                        required=True)

    parser.add_argument("-int_b_m_tn", "--interactor-b-molecule-type-mi-term-name",
                        help="<MI term name entity type of interactor B> [mandatory]",
                        type=str,
                        dest="interactor_b_molecule_type_mi_term_name",
                        action="store",
                        required=True)

    parser.add_argument("-int_det_m", "--interaction-detection-method",
                        help="<comma separated list of the detection methods of the interaction> [optional]",
                        type=str,
                        dest="interaction_detection_method",
                        action="store",
                        required=False)

    parser.add_argument("-int_type_id", "--interaction-type-mi-id",
                        help="<comma separated list of MI IDs of the interaction type> [optional]",
                        type=str,
                        dest="interaction_type_mi_id",
                        action="store",
                        required=False)

    parser.add_argument("-db", "--source-db-mi-id",
                        help="<comma separated list of MI IDs of the database sources> [optional]",
                        type=str,
                        dest="source_db_mi_id",
                        action="store",
                        required=False)

    parser.add_argument("-pmid", "--pubmed-id",
                        help="<comma separated list of pubmed IDs of the paper> [optional]",
                        type=str,
                        dest="pubmed_id",
                        action="store",
                        required=False)

    results = parser.parse_args(args)

    return results.input_file, results.interactor_a_id_type.lower(), results.interactor_b_id_type.lower(), \
           results.interactor_a_tax_id, results.interactor_a_molecule_type_mi_id, \
           results.interactor_a_molecule_type_mi_term_name.lower(), results.interactor_b_molecule_type_mi_id, \
           results.interactor_b_molecule_type_mi_term_name.lower(), results.interaction_detection_method, \
           results.interaction_type_mi_id, results.source_db_mi_id, results.pubmed_id


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR! the specified input file doesn't exists: {input_file}")
        sys.exit(1)


def write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_a_molecule_type_mi_id,
                    interactor_a_molecule_type_mi_term_name, interactor_b_molecule_type_mi_id,
                    interactor_b_molecule_type_mi_term_name, interaction_detection_method,
                    interaction_type_mi_id, source_db_mi_id, pubmed_id, out):

    json_dictionary = {}
    json_dictionary["interactor_a_id"] = line[0].split(":")[1].lower()
    json_dictionary["interactor_b_id"] = line[1].split(":")[1].lower()
    json_dictionary["interactor_a_id_type"] = interactor_a_id_type
    json_dictionary["interactor_b_id_type"] = interactor_b_id_type
    json_dictionary["interactor_b_tax_id"] = int(line[10].split(":")[1].split("(")[0])
    json_dictionary["interactor_a_molecule_type_mi_id"] = interactor_a_molecule_type_mi_id
    json_dictionary["interactor_b_molecule_type_mi_id"] = interactor_b_molecule_type_mi_id
    json_dictionary["interactor_a_molecule_type_name"] = interactor_a_molecule_type_mi_term_name
    json_dictionary["interactor_b_molecule_type_name"] = interactor_b_molecule_type_mi_term_name
    json_dictionary["interaction_detection_methods_mi_id"] = [int(line[6].split(":")[2].split('"')[0])]
    json_dictionary["interaction_types_mi_id"] = []
    json_dictionary["source_database_mi_id"] = [int(line[12].split(":")[2].split('"')[0])]
    json_dictionary["pmids"] = []

    json_dictionary["source_database_mi_id"].append(10002)

    if interaction_detection_method:
        methods = interaction_detection_method.split(",")

        for method_id in methods:
            if int(method_id) not in json_dictionary["interaction_detection_methods_mi_id"]:
                json_dictionary["interaction_detection_methods_mi_id"].append(int(method_id))

    if interaction_type_mi_id:
        interaction_types = interaction_type_mi_id.split(",")

        for type_id in interaction_types:
            if int(type_id) not in json_dictionary["interaction_types_mi_id"]:
                json_dictionary["interaction_types_mi_id"].append(int(type_id))

    if source_db_mi_id:
        databases = source_db_mi_id.split(",")

        for db_id in databases:
            if int(db_id) not in json_dictionary["source_database_mi_id"]:
                json_dictionary["source_database_mi_id"].append(int(db_id))

    if pubmed_id:
        pm_ids = pubmed_id.split(",")

        for pmid in pm_ids:
            if int(pmid) not in json_dictionary["pmids"]:
                json_dictionary["pmids"].append(int(pmid))

    out.write(json.dumps(json_dictionary) + '\n')


def main():

    input_file, interactor_a_id_type, interactor_b_id_type, interactor_a_tax_id, interactor_a_molecule_type_mi_id, \
    interactor_a_molecule_type_mi_term_name, interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, \
    interaction_detection_method, interaction_type_mi_id, source_db_mi_id, pubmed_id = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: --- Parameters are fine, starting... ---')

    output_folder = input_file.split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id={interactor_a_tax_id}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'inbiomap_db.json')

    with open(input_file, 'r') as f, open(output_file, 'w') as out:

        print(f'MESSSAGE [{strftime("%H:%M:%S")}]: --- Writing interactions to output file: {output_file} ---')
        for line in f:
            line = line.strip().split('\t')
            write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_a_molecule_type_mi_id,
                            interactor_a_molecule_type_mi_term_name, interactor_b_molecule_type_mi_id,
                            interactor_b_molecule_type_mi_term_name, interaction_detection_method,
                            interaction_type_mi_id, source_db_mi_id, pubmed_id, out)

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: --- InBioMap Database Loader script finished successfully! ---')


if __name__ == '__main__':
    main()
