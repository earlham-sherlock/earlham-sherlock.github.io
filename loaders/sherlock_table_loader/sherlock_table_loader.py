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

    parser.add_argument("-t", "--table-name",
                        help="<name of the table what you want to upload to sherlock> [mandatory]",
                        type=str,
                        dest="table_name",
                        action="store",
                        required=True)

    parser.add_argument("-o", "--output-file",
                        help="<path to an output json file> [mandatory]",
                        type=str,
                        dest="output_file",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.table_name, results.output_file


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: The specified input file does not exists: {input_file}')
        sys.exit(1)


def write_to_output(line, column_names, column_types, out):

    type_proc_json = {
        "varchar": lambda x: str(x),
        "[]varchar": lambda x: [str(i) for i in x.split(",")],
        "int": lambda x: int(x),
        "[]int": lambda x: [int(i) for i in x.split(",")],
        "double": lambda x: float(x),
        "[]double": lambda x: [float(i) for i in x.split(",")],
    }

    json_dictionary = {}

    for n in range(0, len(column_names)):

        try:
            checked_val = type_proc_json[column_types[n]](line[n])
            json_dictionary[column_names[n]] = checked_val

        except KeyError:
            pass

        except ValueError:
            pass

    out.write(json.dumps(json_dictionary) + '\n')


def landing_zone_table_definition(column_names_list, column_types_list, table_name):

    type_proc_sql = {
        "varchar": "VARCHAR",
        "[]varchar": "ARRAY<VARCHAR>",
        "int": "INT",
        "[]int": "ARRAY<INT>",
        "double": "DOUBLE",
        "[]double": "ARRAY<DOUBLE>",
    }

    sql_types = []

    for m in range(0, len(column_names_list)):

        sql_types.append(column_names_list[m] + " " + type_proc_sql[column_types_list[m]])

    values_for_sql_query = ", ".join(sql_types)
    landing_zone_sql_query = f"CREATE TABLE IF NOT EXISTS landing.test ({values_for_sql_query}) WITH " \
        f"(format = 'JSON', external_location = 's3a://sherlock/landing_zone/{table_name}');"

    return landing_zone_sql_query


def project_zone_table_definition(table_name):

    project_zone_sql_query = f"CREATE TABLE IF NOT EXISTS project.{table_name} WITH " \
        f"(format = 'ORC') AS SELECT * FROM landing.{table_name};"

    return project_zone_sql_query


def main():

    input_file, table_name, output_file = parse_args(sys.argv[1:])

    check_params(input_file)
    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    with open(input_file, 'r') as i, open(output_file, 'w') as out:

        column_names_list = []
        column_types_list = []

        column_names = i.readline()
        column_names = column_names.strip().split('\t')

        print(f'MESSAGE [{strftime("%H:%M:%S")}]: Collect the names of the columns')
        for name in column_names:
            regex = re.compile('[@!#$%^&*()<>?/\}|{~:]')

            if regex.search(name) is not None:
                sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: '
                                 f'The column name has a special character: {name}')
                sys.exit(3)
            column_names_list.append(name)

        column_types = i.readline()
        column_types = column_types.strip().split('\t')

        print(f'MESSAGE [{strftime("%H:%M:%S")}]: Collect the types of the columns')
        for types in column_types:
            acceptable_types = ["[]varchar", "varchar", "[]int", "int", "[]double", "double"]

            if types not in acceptable_types:
                sys.stderr.write(f'ERROR MESSAGE [{strftime("%H:%M:%S")}]: '
                                 f'The column type is incorrect: {types}')
                sys.exit(4)
            column_types_list.append(types)

        abspath_output_file = os.path.abspath(output_file)
        print(f'MESSAGE [{strftime("%H:%M:%S")}]: Writing results to the output file: {abspath_output_file}')
        for line in i:

            line = line.strip().split('\t')
            write_to_output(line, column_names, column_types_list, out)

        print(f'MESSAGE [{strftime("%H:%M:%S")}]: Creating the landing zone table definiton')
        landing_zone_sql_query = landing_zone_table_definition(column_names_list, column_types_list, table_name)

        print(f'MESSAGE [{strftime("%H:%M:%S")}]: Creating the project zone table definiton')
        project_zone_sql_query = project_zone_table_definition(table_name)

    print(f'MESSAGE [{strftime("%H:%M:%S")}]: Sherlock Table Loader script finished successfully!')


if __name__ == '__main__':
    main()
