import argparse
import sys
import os
import json
import re
from time import strftime


def parse_args(args):
    help_text = \
        """
        === String Database Loader script ===

        **Description:**

        This script takes a String database file, which contains protein-protein
        interactions and converts it to Sherlock compatible JSON format.

        The downloaded database file does not contain some of the parameters below!
        Because of this, the user have to identify these parameters!


        **Parameters:**

        -i, --input-file <path>                                       : path to an existing HINT db file [mandatory]

        -int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A, default: ensembl [optional]

        -int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B, default: ensembl [optional]

        -int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]

        -int_b_tax_id, --interactor-b-tax-id <int>                    : taxonomy ID of interactor B [mandatory]

        -int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A, default: 326 [optional]

        -int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A, default: protein [optional]

        -int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B, default: 326 [optional]

        -int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B, default: protein [optional]

        -int_det_m, --interaction-detection-method <int>              : the detection methods of the interaction, default: 45 [optional]

        -int_type_id, --interaction-type-mi-id <int>                  : the MI IDs of the interaction type, default: 190 [optional]

        -db, --source-db-mi-id <int>                                  : the MI ID of the database sources, default: 1014 [optional]

        -pmid, --pubmed-id <int>                                      : the pubmed IDs of the paper, default: 30476243 [optional]


        **Exit codes**

        Exit code 1: The specified input file does not exists!
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-file",
                        help="<path to an existing String db file> [mandatory]",
                        type=str,
                        dest="input_file",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_id", "--interactor-a-id-type",
                        help="<ID type of interactor A> [optional]",
                        type=str,
                        dest="interactor_a_id_type",
                        action="store",
                        default="ensembl",
                        required=False)

    parser.add_argument("-int_b_id", "--interactor-b-id-type",
                        help="<ID type of interactor B> [optional]",
                        type=str,
                        dest="interactor_b_id_type",
                        action="store",
                        default="ensembl",
                        required=False)

    parser.add_argument("-int_a_tax_id", "--interactor-a-tax-id",
                        help="<taxonomy ID of interactor A> [mandatory]",
                        type=int,
                        dest="interactor_a_tax_id",
                        action="store",
                        required=True)

    parser.add_argument("-int_b_tax_id", "--interactor-b-tax-id",
                        help="<taxonomy ID of interactor B> [mandatory]",
                        type=int,
                        dest="interactor_b_tax_id",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_m_id", "--interactor-a-molecule-type-mi-id",
                        help="<MI ID entity type of interactor A> [optional]",
                        type=int,
                        dest="interactor_a_molecule_type_mi_id",
                        action="store",
                        default=326,
                        required=False)

    parser.add_argument("-int_a_m_tn", "--interactor-a-molecule-type-mi-term-name",
                        help="<MI term name entity type of interactor A> [optional]",
                        type=str,
                        dest="interactor_a_molecule_type_mi_term_name",
                        action="store",
                        default="protein",
                        required=False)

    parser.add_argument("-int_b_m_id", "--interactor-b-molecule-type-mi-id",
                        help="<MI ID entity type of interactor B> [optional]",
                        type=int,
                        dest="interactor_b_molecule_type_mi_id",
                        action="store",
                        default=326,
                        required=False)

    parser.add_argument("-int_b_m_tn", "--interactor-b-molecule-type-mi-term-name",
                        help="<MI term name entity type of interactor B> [mandatory]",
                        type=str,
                        dest="interactor_b_molecule_type_mi_term_name",
                        action="store",
                        default="protein",
                        required=False)

    parser.add_argument("-int_det_m", "--interaction-detection-method",
                        help="<the detection methods of the interaction> [optional]",
                        type=int,
                        dest="interaction_detection_method",
                        action="store",
                        default=45,
                        required=False)

    parser.add_argument("-int_type_id", "--interaction-type-mi-id",
                        help="<the MI IDs of the interaction type> [optional]",
                        type=int,
                        dest="interaction_type_mi_id",
                        action="store",
                        default=190,
                        required=False)

    parser.add_argument("-db", "--source-db-mi-id",
                        help="<the MI ID of the source database> [optional]",
                        type=int,
                        dest="source_db_mi_id",
                        action="store",
                        default=1014,
                        required=False)

    parser.add_argument("-pmid", "--pubmed-id",
                        help="<the pubmed ID of the paper> [optional]",
                        type=int,
                        dest="pubmed_id",
                        action="store",
                        default=30476243,
                        required=False)

    results = parser.parse_args(args)

    return results.input_file, results.interactor_a_id_type.lower(), results.interactor_b_id_type.lower(), \
           results.interactor_a_tax_id, results.interactor_b_tax_id, results.interactor_a_molecule_type_mi_id, \
           results.interactor_a_molecule_type_mi_term_name.lower(), results.interactor_b_molecule_type_mi_id, \
           results.interactor_b_molecule_type_mi_term_name.lower(), results.interaction_detection_method, \
           results.interaction_type_mi_id, results.source_db_mi_id, results.pubmed_id


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR MESSAGE: The specified input file does not exists: {input_file}")
        sys.exit(1)


def write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_b_tax_id,
                    interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                    interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name,
                    interaction_detection_method, interaction_type_mi_id, source_db_mi_id, pubmed_id, out):

    json_dictionary = {}
    json_dictionary["interactor_a_id"] = line[0].split(".")[1].lower()
    json_dictionary["interactor_b_id"] = line[1].split(".")[1].lower()
    json_dictionary["interactor_a_id_type"] = interactor_a_id_type
    json_dictionary["interactor_b_id_type"] = interactor_b_id_type
    json_dictionary["interactor_b_tax_id"] = interactor_b_tax_id
    json_dictionary["interactor_a_molecule_type_mi_id"] = interactor_a_molecule_type_mi_id
    json_dictionary["interactor_b_molecule_type_mi_id"] = interactor_b_molecule_type_mi_id
    json_dictionary["interactor_a_molecule_type_name"] = interactor_a_molecule_type_mi_term_name
    json_dictionary["interactor_b_molecule_type_name"] = interactor_b_molecule_type_mi_term_name
    json_dictionary["combined_score"] = line[2]
    json_dictionary["interaction_detection_methods_mi_id"] = interaction_detection_method
    json_dictionary["interaction_types_mi_id"] = interaction_type_mi_id
    json_dictionary["source_database_mi_id"] = source_db_mi_id
    json_dictionary["pmids"] = pubmed_id

    out.write(json.dumps(json_dictionary) + '\n')


def main():
    input_file, interactor_a_id_type, interactor_b_id_type, interactor_a_tax_id, interactor_b_tax_id, \
    interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name, \
    interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, interaction_detection_method, \
    interaction_type_mi_id, source_db_mi_id, pubmed_id = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    output_folder = input_file.split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id={interactor_a_tax_id}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'string_db.json')
    lines_in_input = sum(1 for line in open(input_file))

    with open(input_file, 'r') as f, open(output_file, 'w') as out:

        f.readline()
        index = 0

        print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Writing interactions to output file: {output_file}')
        for line in f:
            line = line.strip().split(" ")

            percent = int(index / lines_in_input * 100)
            sys.stdout.write(f'\r{index}/{lines_in_input} - {percent}% done!')
            index += 1

            int_a_tax_id = int(line[0].split(".")[0])
            int_b_tax_id = int(line[1].split(".")[0])

            if int_a_tax_id != interactor_a_tax_id and int_b_tax_id != interactor_b_tax_id:
                continue

            write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_b_tax_id,
                            interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                            interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name,
                            interaction_detection_method, interaction_type_mi_id, source_db_mi_id, pubmed_id, out)

    print(f'\nMESSSAGE [{strftime("%H:%M:%S")}]: String Database Loader script finished successfully!')


if __name__ == '__main__':
    main()
