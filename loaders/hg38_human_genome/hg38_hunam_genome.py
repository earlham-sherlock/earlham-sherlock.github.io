import argparse
import sys
import os
from pyfasta import Fasta
import json


def parse_args(args):
    help_text = \
        """
        === Cut Up Genomes script ===
        """

    parser = argparse.ArgumentParser(description=help_text)

    # Comma separated paths of input network files
    parser.add_argument("-i", "--input-files",
                        help="<paths to the input fasta files> [mandatory]",
                        type=str,
                        dest="input_files",
                        action="store",
                        required=True)

    # Output file path
    parser.add_argument("-o", "--output-folder",
                        help="<path to an output folder> [mandatory]",
                        type=str,
                        dest="output_folder",
                        action="store",
                        required=True)

    # Method
    parser.add_argument("-l", "--region-length",
                        help="<the value of the length of the cutting region> [mandatory]",
                        type=int,
                        dest="region_length",
                        action="store",
                        required=True)

    results = parser.parse_args(args)
    return results.input_files, results.output_folder, results.region_length


def check_params(input_files_list, output_folder):
    for input_file in input_files_list:
        if not os.path.isfile(input_file):
            sys.stderr.write(f"ERROR! one of the specified input file doesn't exists: {input_file}")
            sys.exit(1)

        if not input_file.endswith(".fa"):
            sys.stderr.write(f"ERROR! this is not a fasta file: {input_file}")
            sys.exit(2)

    if not os.path.isdir(output_folder):
        sys.stderr.write(f"ERROR! the specified output folder doesn't exists: {output_folder}")
        sys.exit(3)


def write_to_json(path, sequence_pieces, region_length):
    os.mkdir(path)
    json_file = os.path.join(path, f'chromosome.json')
    with open(json_file, "w") as output:
        start = 1
        for region in sequence_pieces:
            dictionary = {}
            dictionary["length"] = len(region)
            dictionary["start"] = start
            dictionary["stop"] = start + len(region) - 1
            dictionary["sequence"] = f'{region}'
            output.write(json.dumps(dictionary) + '\n')
            start = start + region_length


def cut_up_genome(input_files_list, output_folder, region_length):
    for file in input_files_list:
        f = Fasta(file)
        chr = sorted(f.keys())
        for chromosome in chr:
            sequence = f[chromosome]
            regions = [sequence[i:i + region_length] for i in range(0, len(sequence), region_length)]
            path = os.path.join(output_folder, f'chr={chromosome}')
            write_to_json(path, regions, region_length)
            print(f'{chromosome} is complete!')


def main():

    input_files, output_folder, region_length = parse_args(sys.argv[1:])
    input_files_list = input_files.split(',')

    check_params(input_files_list, output_folder)

    cut_up_genome(input_files_list, output_folder, region_length)

    path, filename = os.path.split(input_files_list[0])
    for file in os.listdir(path):
        filenames = os.path.join(path, file)
        if filenames.endswith(".flat"):
            os.remove(filenames)
        elif filenames.endswith(".gdx"):
            os.remove(filenames)

    print(f'====== Cut Up Genomes script finished successfully! ======')


if __name__ == "__main__":
    main()

