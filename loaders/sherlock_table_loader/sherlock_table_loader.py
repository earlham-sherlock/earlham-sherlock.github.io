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

    parser.add_argument("-l", "--location",
                        help="<directory name of the files in the landing zone> [mandatory]",
                        type=str,
                        dest="location",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.header, results.output_file, results.location


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


def landing_zone_table_definition(location, json_column_names, list_or_not, types):

    project_directory = f'../../projects/{location}'
    if not os.path.isdir(project_directory):
        os.mkdir(project_directory)

    landing_zone_file = f'{project_directory}/{location}_landing.sql'

    with open(landing_zone_file, 'w') as landing:

        landing.write(f'CREATE TABLE IF NOT EXISTS landing.{location} (' + '\n')

        for l in range(0, len(json_column_names)):
            if list_or_not[l] == "yes":
                if types[l] == "str":
                    landing.write(f'{json_column_names[l]} ARRAY<VARCHAR>,' + '\n')
                elif types[l] == "int":
                    landing.write(f'{json_column_names[l]} ARRAY<INT>,' + '\n')
                else:
                    landing.write(f'{json_column_names[l]} ARRAY<DOUBLE>,' + '\n')
            else:
                if types[l] == "str":
                    landing.write(f'{json_column_names[l]} VARCHAR,' + '\n')
                elif types[l] == "int":
                    landing.write(f'{json_column_names[l]} INT,' + '\n')
                else:
                    landing.write(f'{json_column_names[l]} DOUBLE,' + '\n')

        landing.write(
            f") WITH (" + '\n' +
            f"format='JSON'," + '\n' +
            f"external_location='s3a://sherlock/landing_zone/{location}');")


def project_zone_table_definition(location):

    project_directory = f'../../projects/{location}'
    project_zone_file = f'{project_directory}/{location}_master.sql'

    order_by = str(input("What do you want to order by? (comma separated list): "))
    order_by_list = order_by.split(",")

    with open(project_zone_file, 'w') as project:

        project.write(f'CREATE TABLE IF NOT EXISTS master.{location} WITH (' + '\n'
                    f"format = 'ORC'" + '\n'
                    f") AS SELECT * FROM landing.{location} ORDER BY {', '.join(order_by_list)};")


def main():

    input_file, header, output_file, location = parse_args(sys.argv[1:])

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

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Creating the landing zone table definition and save it to a file')
    landing_zone_table_definition(location, json_column_names, list_or_not, types)
    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Landing zone table definition is done!')

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Creating the project zone table definition and save it to a file')
    project_zone_table_definition(location)
    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Project zone table definition is done!')

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Sherlock Table Loader script finished successfully!')


if __name__ == '__main__':
    main()
