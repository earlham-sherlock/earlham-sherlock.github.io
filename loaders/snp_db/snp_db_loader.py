import argparse
import sys
import os
import json
from time import strftime


def parse_args(args):
    help_text = \
        """
        === SNP Database Loader script ===

        **Description:**

        This script takes a VCF file from SNP database, which contains SNPs
        and converts it to Sherlock compatible JSON format.
        
        
        **Parameters:**
        
        -i, --input-file <path>                                       : path to an existing VCF SNP db file [mandatory]
        
        -o, --output-folder <path>                                    : path to an output folder [optional]
        
        
        **Exit codes**
        
        Exit code 1: The specified input file does not exists!
        Exit code 2: The specified input file is not a VCF file!
        Exit code 3: The specified output folder does not exists!
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-file",
                        help="<path to an existing VCF SNP db file> [mandatory]",
                        type=str,
                        dest="input_file",
                        action="store",
                        required=True)

    parser.add_argument("-o", "--output-folder",
                        help="<path to an output folder> [mandatory]",
                        type=str,
                        dest="output_folder",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.output_folder


def progress_bar(iteration, total, barLength):
   percent = int((iteration / total) * 100)
   bar_fill = '=' * percent
   bar_empty = ' ' * (barLength - percent)
   actual = bar_fill + bar_empty
   sys.stdout.write(f'\r[{actual}] {iteration} line processed | {percent}%')


def check_params(input_file, output_folder):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR MESSAGE: The specified input file does not exists: {input_file}")
        sys.exit(1)

    if not input_file.endswith(".vcf"):
        sys.stderr.write(f"ERROR MESSAGE: The specified input file is not a VCF file: {input_file}")
        sys.exit(2)

    if not os.path.isdir(output_folder):
        sys.stderr.write(f"ERROR MESSAGE: The specified output folder does not exists: {output_folder}")
        sys.exit(3)


def write_to_json(location, snp_id, reference, alt, output):

    json_dictionary = {}
    json_dictionary["location"] = int(location)
    json_dictionary["snp_id"] = snp_id
    json_dictionary["reference"] = reference
    json_dictionary["alt"] = alt

    output.write(json.dumps(json_dictionary) + '\n')


def main():

    input_file, output_folder = parse_args(sys.argv[1:])

    os.mkdir(output_folder)

    check_params(input_file, output_folder)
    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    lines = 0

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Writing SNPs to output files...')
    with open(input_file, 'r') as f:

        for line in f:

            if line[0] == '#':
                continue

            line = line.strip().split('\t')

            chromosome = line[0]
            location = line[1]
            snp_id = line[2]
            reference = line[3]
            alt = line[4]

            path = os.path.join(output_folder, f'chr=chr{chromosome}')
            if not os.path.isdir(path):
                os.mkdir(path)

            json_file = os.path.join(path, f'dbsnp.json')

            with open(json_file, "a") as output:
                write_to_json(location, snp_id, reference, alt, output)

            lines += 1
            if lines % 50000 == 0:
                progress_bar(lines, 37303035, 100)

    progress_bar(lines, lines, 100)
    print(f'\nMESSAGE [{strftime("%H:%M:%S")}]: SNP Database Loader script finished successfully!')


if __name__ == '__main__':
    main()
