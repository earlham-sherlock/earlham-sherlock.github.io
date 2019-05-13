import argparse
import sys
import os
import json


def parse_args(args):
    help_text = \
        """
        === HINT Database Loader script ===
        
        **Description:**

        This script takes a HINT database file, which contains protein-protein
        interactions and converts it to Sherlock compatible JSON format.
        
        The downloaded database file does not contain the parameters below!
        Because of this, the user have to identify these mandatory parameters!
        
        
        **Parameters:**
        
        -i, --input-file <path>                                       : path to an existing HINT db file [mandatory]
        
        -int_a_id, --interactor-a-id-type <str>                       : ID type of interactor A [mandatory]
        
        -int_b_id, --interactor-b-id-type <str>                       : ID type of interactor B [mandatory]
        
        -int_a_tax_id, --interactor-a-tax-id <int>                    : taxonomy ID of interactor A [mandatory]
        
        -int_b_tax_id, --interactor-b-tax-id <int>                    : taxonomy ID of interactor B [mandatory]
        
        -int_a_m_id, --interactor-a-molecule-type-mi-id <int>         : MI ID entity type of interactor A [mandatory]
        
        -int_a_m_tn, --interactor-a-molecule-type-mi-term-name <str>  : MI term name entity type of interactor A [mandatory]
        
        -int_b_m_id, --interactor-b-molecule-type-mi-id <int>         : MI ID entity type of interactor B [mandatory]
        
        -int_b_m_tn, --interactor-b-molecule-type-mi-term-name <str>  : MI term name entity type of interactor B [mandatory]
        
        -int_type_id, --interaction_type_mi_id <int>                  : MI ID of the interaction type [optional]
        
        
        **Exit codes**
        
        Exit code 1: The specified input file doesn't exists!
        
        
        **Notes**

        1) The HINT database does not include the mi identifiers of the interaction types!
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

    parser.add_argument("-int_b_tax_id", "--interactor-b-tax-id",
                        help="<taxonomy ID of interactor B> [mandatory]",
                        type=int,
                        dest="interactor_b_tax_id",
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

    parser.add_argument("-int_type_id", "--interaction_type_mi_id",
                        help="<MI ID of the interaction type> [mandatory]",
                        type=int,
                        dest="interaction_type_mi_id",
                        action="store",
                        required=False)

    results = parser.parse_args(args)

    return results.input_file, results.interactor_a_id_type.lower(), results.interactor_b_id_type.lower(),\
           results.interactor_a_tax_id, results.interactor_b_tax_id, results.interactor_a_molecule_type_mi_id,\
           results.interactor_a_molecule_type_mi_term_name.lower(), results.interactor_b_molecule_type_mi_id,\
           results.interactor_b_molecule_type_mi_term_name.lower(), results.interaction_type_mi_id


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR! the specified input file doesn't exists: {input_file}")
        sys.exit(1)


def write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_b_tax_id,
                    interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                    interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, interaction_type_mi_id,
                    out):

    json_dictionary = {}
    json_dictionary["interactor_a_id"] = line[0].lower()
    json_dictionary["interactor_b_id"] = line[1].lower()
    json_dictionary["interactor_a_id_type"] = interactor_a_id_type
    json_dictionary["interactor_b_id_type"] = interactor_b_id_type
    json_dictionary["interactor_b_tax_id"] = interactor_b_tax_id
    json_dictionary["interactor_a_molecule_type_mi_id"] = interactor_a_molecule_type_mi_id
    json_dictionary["interactor_b_molecule_type_mi_id"] = interactor_b_molecule_type_mi_id
    json_dictionary["interactor_a_molecule_type_name"] = interactor_a_molecule_type_mi_term_name
    json_dictionary["interactor_b_molecule_type_name"] = interactor_b_molecule_type_mi_term_name
    json_dictionary["interaction_detection_methods_mi_id"] = []
    json_dictionary["interaction_types_mi_id"] = []
    json_dictionary["source_database_mi_id"] = [10000]
    json_dictionary["pmids"] = []

    info = line[8].split("|")

    for i in info:

        detection_method = i.split(":")[1]
        pm_id = i.split(":")[0]

        json_dictionary["interaction_detection_methods_mi_id"].append(int(detection_method))
        json_dictionary["pmids"].append(pm_id)

    if interaction_type_mi_id:
        json_dictionary["interaction_types_mi_id"].append(interaction_type_mi_id)

    out.write(json.dumps(json_dictionary) + '\n')


def main():

    input_file, interactor_a_id_type, interactor_b_id_type, interactor_a_tax_id, interactor_b_tax_id,\
    interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,\
    interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name, interaction_type_mi_id\
    = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSSAGE: --- Parameters are fine, starting... ---')

    output_folder = input_file.split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id={interactor_a_tax_id}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'hint_db.json')

    with open(input_file, 'r') as f, open(output_file, 'w') as out:

        f.readline()

        print(f'MESSSAGE: --- Writing interactions to output file: {output_file} ---')
        for line in f:
            line = line.strip().split('\t')
            write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_b_tax_id,
                            interactor_a_molecule_type_mi_id, interactor_a_molecule_type_mi_term_name,
                            interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name,
                            interaction_type_mi_id, out)

    print(f'MESSSAGE: --- HINT Database Loader script finished successfully! ---')


if __name__ == '__main__':
    main()
