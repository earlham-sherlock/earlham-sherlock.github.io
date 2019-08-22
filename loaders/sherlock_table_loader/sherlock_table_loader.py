import argparse
import sys
import os
import json
from time import strftime


def parse_args(args):
    help_text = \
        """
        === Sherlock Table Loader script ===
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-file",
                        help="<path to an existing TSV/CSV/MITAB file> [mandatory]",
                        type=str,
                        dest="input_file",
                        action="store",
                        required=True)

    parser.add_argument("-hea", "--header",
                        help="<a number that shows how many header lines the input file has> [mandatory]",
                        type=int,
                        dest="header",
                        action="store",
                        required=True)

    parser.add_argument("-o", "--output-file",
                        help="<path to an output file> [mandatory]",
                        type=str,
                        dest="output_file",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.header, results.output_file


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: The specified input file does not exists: {input_file}')
        sys.exit(1)


def collect_needed_information(needed_columns, json_column_names, list_or_not, delimiter, types):

    column_number = int(input("Number of the column? (Note: numbering of the columns starts with 0!): "))
    needed_columns.append(column_number)

    column_name = str(input("Name of the given column in the output json file?: "))
    json_column_names.append(column_name)

    column_list = str(input("Is this given column a list or not? (yes or no): "))

    if column_list == "Yes" or column_list == "yes" or column_list == "y":
        list_or_not.append("yes")
        list_delimiter = str(input("What is the delimiter in this list?: "))
        delimiter.append(list_delimiter)

    else:
        list_or_not.append("no")
        delimiter.append(None)

    column_type = str(input("Type of the given column? (str for string, int for integer or float): "))
    accepted_types = ["str", "int", "float"]
    if column_type in accepted_types:
        types.append(column_type)
    else:
        sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: Type what you gave is not correct: {column_type}')
        sys.exit(2)


def write_to_output(line, out, needed_columns, json_column_names, list_or_not, delimiter, types):

    json_dictionary = {}

    for m in range(0, len(needed_columns)):
        if list_or_not[m] == "yes":
            json_list = line[needed_columns[m]].split(delimiter[m])
            json_dictionary[json_column_names[m]] = []
            for member in json_list:
                if types[m] == "int":
                    json_dictionary[json_column_names[m]].append(int(member))
                elif types[m] == "float":
                    json_dictionary[json_column_names[m]].append(float(member))
                else:
                    json_dictionary[json_column_names[m]].append(member)
        else:
            if types[m] == "int":
                json_dictionary[json_column_names[m]] = int(line[needed_columns[m]])
            elif types[m] == "float":
                json_dictionary[json_column_names[m]] = float(line[needed_columns[m]])
            else:
                json_dictionary[json_column_names[m]] = line[needed_columns[m]]

    out.write(json.dumps(json_dictionary) + '\n')


def main():

    input_file, header, output_file = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    needed_columns = []
    json_column_names = []
    list_or_not = []
    delimiter = []
    types = []

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Collecting needed information form the input file {input_file}\n')

    collect_needed_information(needed_columns, json_column_names, list_or_not, delimiter, types)

    for x in range(0, 10000):

        question = str(input("\nDo you want to select an other column and add it to the output json file? (yes or no): "))
        if question == "No" or question == "no" or question == "n":
            break

        collect_needed_information(needed_columns, json_column_names, list_or_not, delimiter, types)

    print(f'Your selected columns from the input file: {needed_columns}\nYour selected names of the columns: {json_column_names}')

    abs_output_filepath = os.path.abspath(output_file)
    print(f'\nMESSAGE [{strftime("%H:%M:%S")}]: Writing results to the output json file {abs_output_filepath}')
    with open(input_file, 'r') as i, open(output_file, 'w') as out:

        if header != 0:
            for n in range(0, header):
                i.readline()

        for line in i:
            line = line.strip().split("\t")
            write_to_output(line, out, needed_columns, json_column_names, list_or_not, delimiter, types)

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Sherlock Table Loader script finished successfully!')


if __name__ == '__main__':
    main()
