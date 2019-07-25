import argparse
import sys
import os
import json
import pandas as pd
from time import strftime


def parse_args(args):
    help_text = \
        """
        === Sherlock Ortholog Mapper Loader script ===
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-files-list",
                        help="<comma separated paths to existing files> [mandatory]",
                        type=str,
                        dest="input_files_list",
                        action="store",
                        required=True)

    parser.add_argument("-f", "--from-tax-id",
                        help="<taxonomy identifier of source> [mandatory]",
                        type=int,
                        dest="from_tax_id",
                        action="store",
                        required=True)

    parser.add_argument("-t", "--to-tax-ids",
                        help="<comma separated taxonomy identifiers of targets> [mandatory]",
                        type=str,
                        dest="to_tax_ids",
                        action="store",
                        required=True)

    parser.add_argument("-o", "--output-folder",
                        help="<path to an output folder> [mandatory]",
                        type=str,
                        dest="output_folder",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_files_list, results.from_tax_id, results.to_tax_ids, results.output_folder


def check_params(input_files_list):

    for input_file in input_files_list:
        if not os.path.isfile(input_file):
            sys.stderr.write(f"ERROR MESSAGE: The specified input file does not exists: {input_file}")
            sys.exit(1)


def write_to_output(line, to_tax_id, out):

    json_dictionary = {}

    json_dictionary["to_tax_id"] = int(to_tax_id)
    json_dictionary["from_id"] = line[0].split('_')[0].lower()
    json_dictionary["to_id"] = line[1].split('_')[0].lower()
    json_dictionary["orthology_type"] = line[2]
    json_dictionary["oma_group"] = int(line[3].split(".")[0])

    out.write(json.dumps(json_dictionary) + '\n')


def main():

    input_files_list, from_tax_id, to_tax_ids, output_folder = parse_args(sys.argv[1:])

    to_tax_identifiers = to_tax_ids.split(",")
    input_files = input_files_list.split(",")

    check_params(input_files)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')
    if len(to_tax_identifiers) != len(input_files):
        sys.stderr.write(f"ERROR MESSAGE: The number of the input files and the number of the to taxonomy IDs must be equal")
        sys.exit(2)

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    new_folder = os.path.join(output_folder, f'from_tax_id={from_tax_id}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'ortholog_mapping.json')
    abspath_output_file = os.path.abspath(output_file)

    for index in range(0, len(input_files)):
        to_tax_id = to_tax_identifiers[index]
        input_file = input_files[index]
        matrix = pd.read_csv(input_file, sep='\t', names=['from_tax_id', 'to_tax_id', 'orthology_type', 'oma_group'])
        matrix = matrix.dropna()
        helper_file = f"only_oma_groups.txt"
        matrix.to_csv(helper_file, sep='\t', header=False, index=False)

        with open(helper_file, 'r') as f, open(output_file, 'w') as out:

            print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Writing interactions to output file: {abspath_output_file}')
            for line in f:
                line = line.strip().split('\t')
                write_to_output(line, to_tax_id, out)

        os.remove(helper_file)

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Sherlock Ortholog Mapper Loader script finished successfully!')


if __name__ == '__main__':
    main()
