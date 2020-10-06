import argparse
import sys
import os
import json
import re
from time import strftime


def parse_args(args):
    help_text = \
        """
        === Dorothea Database Loader script ===
        
        **Description:**

        This script takes a HINT database file, which contains protein-protein
        interactions and converts it to Sherlock compatible JSON format.
        
        The downloaded database file does not contain some of the parameters below!
        Because of this, the user have to identify these parameters!
        
        **Parameters:**
        
        -i, --input-file <path>                                       : path to an existing HINT db file [mandatory]        
        
        **Exit codes**
        
        Exit code 1: The specified input file does not exists!
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-file",
                        help="<path to an existing dorothea db file> [mandatory]",
                        type=str,
                        dest="input_file",
                        action="store",
                        required=True)

    parser.add_argument("-int_a_id", "--interactor-a-id-type",
                        help="<ID type of interactor A> [mandatory]",
                        type=str,
                        dest="interactor_a_id_type",
                        action="store",
                        default="uniprotac",
                        required=False)

    parser.add_argument("-int_b_id", "--interactor-b-id-type",
                        help="<ID type of interactor B> [mandatory]",
                        type=str,
                        dest="interactor_b_id_type",
                        action="store",
                        default="uniprotac",
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

    parser.add_argument("-v", "--version",
                        help="<version (date) of the downloaded file> [mandatory]",
                        type=str,
                        dest="version",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.interactor_a_id_type.lower(), results.interactor_b_id_type.lower(), \
           results.interactor_a_tax_id, results.interactor_b_tax_id, results.version


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR MESSAGE: The specified input file does not exists: {input_file}")
        sys.exit(1)


def main():

    input_file, interactor_a_id_type, interactor_b_id_type, interactor_a_tax_id, interactor_b_tax_id, version = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    output_folder = f'dorothea_{version}'
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id={interactor_a_tax_id}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'dorothea_db.json')

    with open(input_file, 'r') as dorothea, open(output_file, 'w') as out:

        dorothea.readline()

        for line in dorothea:
            line = line.strip().split('\t')

            json_dictionary = {}
            json_dictionary["interactor_a_id"] = line[0].lower()
            json_dictionary["interactor_b_id"] = line[2].lower()
            json_dictionary["interactor_a_id_type"] = interactor_a_id_type
            json_dictionary["interactor_b_id_type"] = interactor_b_id_type
            json_dictionary["interactor_b_tax_id"] = interactor_b_tax_id
            json_dictionary["confidence_score"] = line[1]
            json_dictionary["mor"] = [int(line[3])]

            out.write(json.dumps(json_dictionary) + '\n')

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Dorothea Database Loader script finished successfully!')


if __name__ == '__main__':
    main()
