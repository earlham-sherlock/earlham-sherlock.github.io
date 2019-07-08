import argparse
import sys
import os
import re
import json
from collections import defaultdict
from time import strftime


def parse_args(args):
    help_text = \
        """
        === Gene Ontology Loader script ===
        """

    parser = argparse.ArgumentParser(description=help_text)

    parser.add_argument("-i", "--input-file",
                        help="<path to an existing .obo file> [mandatory]",
                        type=str,
                        dest="input_file",
                        action="store",
                        required=True)

    parser.add_argument("-wd", "--working-directory",
                        help="<path to an existing folder, where the script can work in> [mandatory]",
                        type=str,
                        dest="working_directory",
                        action="store",
                        required=True)

    results = parser.parse_args(args)

    return results.input_file, results.working_directory


def check_params(input_file):

    if not os.path.isfile(input_file):
        sys.stderr.write(f"ERROR MESSAGE: The specified input file does not exists: {input_file}")
        sys.exit(1)

    if not input_file.endswith(".obo"):
        sys.stderr.write(f"ERROR MESSAGE: The specified input file is not an OBO file: {input_file}")
        sys.exit(2)


def get_terms_per_line(input_file, helper_file, go_ids):

    array = []
    id_pattern = '(id: GO:([0-9]{7}))'

    with open(input_file, 'r') as f, open(helper_file, 'w') as out:

        term_array = []

        for line in f:
            line = line.strip()

            key_words = ['format-version', 'data-version', 'subsetdef', 'synonymtypedef', 'default-namespace',
                        'remark', 'ontology', 'property_value']

            if any(ext in line for ext in key_words):
                continue

            if line.startswith("[Term]") or line.startswith("[Typedef]"):
                term_array = []
                continue

            if line != "":
                term_array.append(line)

            elif line == "":
                array.append(term_array)

            if "id: GO:" in line and "alt_id: GO:" not in line:
                id = re.findall(id_pattern, line)
                if id:
                    if id not in go_ids:
                        go_ids.append(id[0][1])

        for member in array:

            if member != []:
                if "id: GO:" not in member[0]:
                    continue
                else:
                    out.write("|".join(member) + '\n')


def get_direct_parents(go_ids, helper_file):

    parents_dictionary = {}
    pattern = '(is_a: GO:([0-9]{7}))'
    pattern2 = '(part_a: GO:([0-9]{7}))'

    with open(helper_file, 'r') as f2:

        for row in f2:
            row = row.strip()

            identifier = row.split("|")[0].split(":")[2]

            if identifier in go_ids:
                if "is_a" in row or "part_of" in row:
                    parents = re.findall(pattern, row)
                    parents2 = re.findall(pattern2, row)

                    for i in range(0, len(parents)):
                        if identifier not in parents_dictionary:
                            parents_dictionary[identifier] = []

                        if len(parents) > 0:
                            if parents[i][1] not in parents_dictionary[identifier]:
                                parents_dictionary[identifier].append(parents[i][1])

                        if len(parents2) > 0:
                            if parents2[i][1] not in parents_dictionary[identifier]:
                                parents_dictionary[identifier].append(parents2[i][1])

    return parents_dictionary


def get_direct_children(parents_dictionary):

    children_dictionary = {}

    for keys, values in parents_dictionary.items():

        for value in values:

            if value not in children_dictionary:
                children_dictionary[value] = []

            if keys not in children_dictionary[value]:
                children_dictionary[value].append(keys)

    return children_dictionary


def get_all_relations(go_ids, given_dictionary):

    return_relations = defaultdict(list)

    for term in go_ids:

        all_relations = []
        if term in given_dictionary:
            all_relations.extend(given_dictionary[term])
        all_relations_to_check = []
        if term in given_dictionary:
            all_relations_to_check.extend(given_dictionary[term])

        while len(all_relations_to_check) > 0:
            all_relations_to_check_add = []
            for relations_to_check in all_relations_to_check:
                if relations_to_check in given_dictionary:
                    all_relations_to_check_add.extend(given_dictionary[relations_to_check])
            all_relations_to_check = []
            all_relations_to_check = list(set(all_relations_to_check_add))
            all_relations.extend(all_relations_to_check)
        return_relations[term] = list(set(all_relations))

    return return_relations


def get_relatives_ids(id, dictionary):

    array = []

    if id in dictionary:
        for value in dictionary[id]:
            if value not in array:
                array.append(int(value))

    return array


def write_to_output(helper_file, parents_dictionary, children_dictionary, all_parents_dictionary,
                    all_children_dictionary, output_file):

    with open(helper_file, 'r') as f, open(output_file, 'w') as out:

        for line in f:
            line = line.strip().split('|')

            id = line[0].split(":")[2]
            name = line[1].split(" ")[1]
            namespace = line[2].split(" ")[1]

            json_dictionary = {}
            json_dictionary["id"] = int(id)
            json_dictionary["id_type"] = "GO"
            json_dictionary["name"] = name
            json_dictionary["namespace"] = namespace
            json_dictionary["alt_ids"] = []
            json_dictionary["direct_parents"] = []
            json_dictionary["direct_children"] = []
            json_dictionary["all_parents"] = []
            json_dictionary["all_children"] = []

            for columns in line:
                alt_id_pattern = '(alt_id: GO:([0-9]{7}))'

                alt_ids = re.findall(alt_id_pattern, columns)

                if alt_ids:
                    json_dictionary["alt_ids"].append(int(alt_ids[0][1]))

            if id in parents_dictionary:
                for member_in_parents_dictionary in parents_dictionary[id]:
                    json_dictionary["direct_parents"].append(int(member_in_parents_dictionary))

            if id in children_dictionary:
                for member_in_children_dictionary in children_dictionary[id]:
                    json_dictionary["direct_children"].append(int(member_in_children_dictionary))

            all_parents_array = get_relatives_ids(id, all_parents_dictionary)
            if len(all_parents_array) > 0:
                json_dictionary["all_parents"] = all_parents_array

            all_children_array = get_relatives_ids(id, all_children_dictionary)
            if len(all_children_array) > 0:
                json_dictionary["all_children"] = all_children_array

            out.write(json.dumps(json_dictionary) + '\n')


def main():

    input_file, working_directory = parse_args(sys.argv[1:])

    if not os.path.isdir(working_directory):
        os.mkdir(working_directory)

    check_params(input_file)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Parameters are fine, starting...')

    go_ids = []
    helper_file = os.path.join(working_directory, "helper.txt")
    abspath_helper_file = os.path.abspath(helper_file)
    output_file = os.path.join(working_directory, "go.json")
    abspath_output_file = os.path.abspath(output_file)

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Creating an intermedier (helper) file: {abspath_helper_file}')
    get_terms_per_line(input_file, helper_file, go_ids)

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Get all the directed parents of each term')
    parents_dictionary = get_direct_parents(go_ids, helper_file)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Get all the directed children of each term')
    children_dictionary = get_direct_children(parents_dictionary)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Get all parents of each term')
    all_parents_dictionary = get_all_relations(go_ids, parents_dictionary)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Get all children of each term')
    all_children_dictionary = get_all_relations(go_ids, children_dictionary)

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Writing results to output file: {abspath_output_file}')
    write_to_output(helper_file, parents_dictionary, children_dictionary, all_parents_dictionary,
                    all_children_dictionary, output_file)

    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Deleting the intermedier file')
    os.remove(helper_file)
    print(f'MESSSAGE [{strftime("%H:%M:%S")}]: Gene Ontology Loader script finished successfully!')


if __name__ == '__main__':
    main()
