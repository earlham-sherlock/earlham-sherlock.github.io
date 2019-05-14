import argparse
import sys
import os
import json


def parse_args(args):
    help_text = \
        """
        === InBioMap Database Loader script ===
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

    results = parser.parse_args(args)

    return results.input_file, results.interactor_a_id_type.lower(), results.interactor_b_id_type.lower(), \
           results.interactor_a_molecule_type_mi_id, results.interactor_a_molecule_type_mi_term_name.lower(), \
           results.interactor_b_molecule_type_mi_id, results.interactor_b_molecule_type_mi_term_name.lower()


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR! the specified input file doesn't exists: {input_file}")
        sys.exit(1)


def write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_a_molecule_type_mi_id,
                    interactor_a_molecule_type_mi_term_name, interactor_b_molecule_type_mi_id,
                    interactor_b_molecule_type_mi_term_name, out):

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
    json_dictionary["source_database_mi_id"] = [10002]
    json_dictionary["pmids"] = []

    out.write(json.dumps(json_dictionary) + '\n')


def main():

    input_file, interactor_a_id_type, interactor_b_id_type, interactor_a_molecule_type_mi_id,\
    interactor_a_molecule_type_mi_term_name, interactor_b_molecule_type_mi_id, interactor_b_molecule_type_mi_term_name,\
    = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSSAGE: --- Parameters are fine, starting... ---')

    output_folder = input_file.split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, "interactor_a_tax_id=9606")
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'inbiomap_db.json')

    with open(input_file, 'r') as f, open(output_file, 'w') as out:

        print(f'MESSSAGE: --- Writing interactions to output file: {output_file} ---')
        for line in f:
            line = line.strip().split('\t')
            write_to_output(line, interactor_a_id_type, interactor_b_id_type, interactor_a_molecule_type_mi_id,
                            interactor_a_molecule_type_mi_term_name, interactor_b_molecule_type_mi_id,
                            interactor_b_molecule_type_mi_term_name, out)

    print(f'MESSSAGE: --- InBioMap Database Loader script finished successfully! ---')


if __name__ == '__main__':
    main()
