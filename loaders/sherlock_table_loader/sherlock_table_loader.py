import argparse
import sys
import os
import re
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

    parser.add_argument("-o", "--output-file",
                        help="<path to an output json file> [mandatory]",
                        type=str,
                        dest="output_file",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.output_file


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: The specified input file does not exists: {input_file}')
        sys.exit(1)


def write_to_output(line, column_names, column_types, out):

    json_dictionary = {}

    for x in range(0, len(column_names)):

        if '[]' in column_types[x]:

            json_dictionary[column_names[x]] = []
            list_values = line[x].split(",")
            for value in list_values:

                if 'str' in column_types[x]:
                    json_dictionary[column_names[x]].append(str(value))

                elif 'int' in column_types[x]:
                    json_dictionary[column_names[x]].append(int(value))

                elif 'float' in column_types[x]:
                    json_dictionary[column_names[x]].append(float(value))

        else:

            if 'str' in column_types[x]:
                json_dictionary[column_names[x]] = str(line[x])

            elif 'int' in column_types[x]:
                json_dictionary[column_names[x]] = int(line[x])

            elif 'float' in column_types[x]:
                json_dictionary[column_names[x]] = float(line[x])

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

    input_file, output_file = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    with open(input_file, 'r') as i, open(output_file, 'w') as out:

        index = 1
        column_names = []
        column_types = []

        for line in i:
            line = line.strip().split('\t')

            if len(line) == 0:
                sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: '
                                 f'The input file has not comma separated values in the {index}. line!')
                sys.exit(2)

            if index == 1:

                for name in line:
                    regex = re.compile('[@!#$%^&*()<>?/\}|{~:]')
                    if regex.search(name) is not None:
                        sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: '
                                         f'The column name has a special character: {name}')
                        sys.exit(3)
                    column_names.append(name)

            elif index == 2:

                for types in line:
                    column_types.append(types)

            else:
                write_to_output(line, column_names, column_types, out)

            index += 1

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Sherlock Table Loader script finished successfully!')


if __name__ == '__main__':
    main()
