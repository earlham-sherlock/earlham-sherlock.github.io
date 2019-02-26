import argparse
import sys
import os
import json
import re
import sqlite3
from sqlite3 import Error


def parse_args(args):
    help_text = \
        """
        === SignaLink3 SQL Loader script ===
        
        **Description:**

        This script takes a SignaLinK 3 compatible SQLite DB file, and converts it to Sherlock compatible JSON format.
        Most of the JSON attributes are taken from the DB file, but some of them are provided as input parameters.
        The script automatically create an output .json file in the output folder. The name of the output .json file will be
        the same as the input SLK3 database file.
        
        
        **Parameters:**
        
        -i, --input-db-file <path>                                  : path to an SLK3 .db file [mandatory]
        
        -int_a_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A [mandatory]
        
        -int_a_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A [mandatory]
        
        -int_b_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B [mandatory]
        
        -int_b_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B [mandatory]
        
        -db, --source-database-mi-id <int>                          : single MI ID of the database [optional]
        
        -o, --output-folder <path>                                  : path to an output folder [mandatory]
        
        
        **Exit codes**
        
        Exit code 1: The specified input SLK3 database file doesn't exists!
        Exit code 2: The specified input SLK3 database file is not a .db file!
        Exit code 3: The specified output folder doesn't exists!
        """

    parser = argparse.ArgumentParser(description=help_text)

    # Input SLK3 database file
    parser.add_argument("-i", "--input-db-file",
                        help="<path to an SLK3 .db file> [mandatory]",
                        type=str,
                        dest="input_db_file",
                        action="store",
                        required=True)

    # Interactor A molecule type mi id
    parser.add_argument("-int_a_id", "--interactor-a-molecule-type-mi-id",
                        help="<MI ID entity type of interactor A> [mandatory]",
                        type=int,
                        dest="interactor_a_molecule_type_mi_id",
                        action="store",
                        required=True)

    # Interactor A molecule type mi term name
    parser.add_argument("-int_a_tn", "--interactor-a-molecule-type-mi-term-name",
                        help="<MI term name entity type of interactor A> [mandatory]",
                        type=str,
                        dest="interactor_a_molecule_type_mi_term_name",
                        action="store",
                        required=True)

    # Interactor B molecule type mi id
    parser.add_argument("-int_b_id", "--interactor-b-molecule-type-mi-id",
                        help="<MI ID entity type of interactor B> [mandatory]",
                        type=int,
                        dest="interactor_b_molecule_type_mi_id",
                        action="store",
                        required=True)

    # Interactor B molecule type mi term name
    parser.add_argument("-int_b_tn", "--interactor-b-molecule-type-mi-term-name",
                        help="<MI term name entity type of interactor B> [mandatory]",
                        type=str,
                        dest="interactor_b_molecule_type_mi_term_name",
                        action="store",
                        required=True)

    # Source DB
    parser.add_argument("-db", "--source-db-mi-id",
                        help="<single MI ID of the database> [mandatory]",
                        type=int,
                        dest="source_db_mi_id",
                        action="store",
                        required=False,
                        default=[""])

    # Output folder path
    parser.add_argument("-o", "--output-folder",
                        help="<path to an output folder> [mandatory]",
                        type=str,
                        dest="output_folder",
                        action="store",
                        required=True)

    results = parser.parse_args(args)
    return results.input_db_file, results.interactor_a_molecule_type_mi_id,\
           results.interactor_a_molecule_type_mi_term_name.lower(), results.interactor_b_molecule_type_mi_id, \
           results.interactor_b_molecule_type_mi_term_name.lower(), results.source_db_mi_id, results.output_folder


def check_params(input_db_file, output_folder):

    if not os.path.isfile(input_db_file):
        sys.stderr.write(f"ERROR! the specified input SLK3 database file doesn't exists: "
                         f"{input_db_file}")
        sys.exit(1)

    if not input_db_file.endswith(".db"):
        sys.stderr.write(f"ERROR! the specified input SLK3 database file is not a .db file: "
                         f"{input_db_file}")
        sys.exit(2)

    if not os.path.isdir(output_folder):
        sys.stderr.write(f"ERROR! the specified output folder doesn't exists: {output_folder}")
        sys.exit(3)


def create_connection(db_file):

    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)

    return None


def select_from_db_file(connection, interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                            interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, source_db_mi_id,
                            output):

    cur = connection.cursor()
    cur.execute("SELECT a.name AS a_name, b.name AS b_name, a.tax_id AS a_taxid, b.tax_id AS b_taxid, "
                "interaction_detection_method, interaction_types, publication_ids FROM edge LEFT JOIN node a "
                "ON edge.interactor_a_node_id = a.id LEFT JOIN node b ON edge.interactor_b_node_id = b.id;")

    lines = cur.fetchall()

    for line in lines:
        write_to_output(line, interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                            interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, source_db_mi_id,
                            output)


def write_to_output(line, interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                            interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, source_db_mi_id,
                            output):

    json_dictionary = {}
    json_dictionary["interactor_a_id"] = line[0].split(":")[1].lower()
    json_dictionary["interactor_b_id"] = line[1].split(":")[1].lower()
    json_dictionary["interactor_a_id_type"] = line[0].split(":")[0].lower()
    json_dictionary["interactor_b_id_type"] = line[1].split(":")[0].lower()
    json_dictionary["interactor_a_tax_id"] = line[2].split(":")[1]
    json_dictionary["interactor_b_tax_id"] = line[3].split(":")[1]
    json_dictionary["interactor_a_molecule_type_mi_id"] = interactor_a_molecule_type_mi_id
    json_dictionary["interactor_b_molecule_type_mi_id"] = interactor_b_molecule_type_mi_id
    json_dictionary["interactor_a_molecule_type_name"] = interactor_a_molecule_type_mi_term_name
    json_dictionary["interactor_b_molecule_type_name"] = interactor_b_molecule_type_mi_term_name

    json_dictionary["interaction_detection_methods_mi_id"] = []
    if line[4] is not None:
        interaction_detection_ids = re.findall('\d+', line[5].strip())
        for detection_id in interaction_detection_ids:
            json_dictionary["interaction_detection_methods_mi_id"].append(int(detection_id))

    json_dictionary["interaction_types_mi_id"] = []
    if line[5] is not None:
        interaction_types_mi_ids = re.findall('\d+', line[5].strip())
        for interaction_id in interaction_types_mi_ids:
            json_dictionary["interaction_types_mi_id"].append(int(interaction_id))

    json_dictionary["source_database_mi_id"] = []
    if source_db_mi_id:
        json_dictionary["source_database_mi_id"] = [source_db_mi_id]

    json_dictionary["pmids"] = []
    if line[6] is not None:
        json_dictionary["pmids"] = [int(line[6].split(":")[1])]

    output.write(json.dumps(json_dictionary) + '\n')


def main():

    input_db_file, interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name, \
    interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, source_db_mi_id, \
    output_folder = parse_args(sys.argv[1:])

    check_params(input_db_file, output_folder)
    print(f'====== Parameters are fine, starting... ======')

    connection = create_connection(input_db_file)
    with connection:
        new_file = f'{input_db_file.split("/")[-1].split(".")[0].strip()}.json'
        output_json_file = os.path.join(output_folder, new_file)
        with open(output_json_file, 'w') as output:
            print(f'====== Write results to output file: {output_json_file} ======')
            select_from_db_file(connection, interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                                interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, source_db_mi_id,
                                output)

    print(f'====== SingaLink3 SQL Loader script finished successfully! ======')


if __name__ == '__main__':
    main()
