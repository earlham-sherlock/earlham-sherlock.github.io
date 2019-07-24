import sys
import argparse
import pandas as pd


class DuplicatedIdentifiers(Exception):
    pass


def parse_args(argv):
    """ Command line interface for the single-cell pipeline. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database')
    parser.add_argument('-m', '--matrix')
    parser.add_argument('-o', '--output')
    parser.add_argument('-d', '--debug', required=False, default=False)
    return parser.parse_args(argv[1:])


def map_and_concat(database, matrix):
    """ Remap the speciesID A to speciesID B """
    for idx, interaction in enumerate(database):
        inter_a_id = interaction["interactor_a_id"].upper()
        inter_b_id = interaction["interactor_b_id"].upper()
        mouse_a_id = matrix.get(inter_a_id, ['-'])
        mouse_b_id = matrix.get(inter_b_id, ['-'])
        database[idx]['mapped_inter_id_a'] = mouse_a_id[0]
        database[idx]['mapped_inter_id_b'] = mouse_b_id[0]
    return database


def main(argv):
    """ Main method for single-cell omix pipeline """
    args = parse_args(argv)
    database = pd.read_json(args.database, lines=True)
    database = database.append(pd.DataFrame(columns=['mapped_inter_id_a', 'mapped_inter_id_b']))
    matrix = pd.read_csv(args.matrix, sep='\t', names=['tax_current', 'tax_convert', 'link', 'oma'])
    matrix = matrix.dropna()
    output_stirng = f"mapped-human-mouse-uniprot.txt"
    matrix.to_csv(output_stirng, sep='\t', header=False, index=False)

    if len(matrix[matrix.duplicated()].values) > 0:
        raise DuplicatedIdentifiers()
    else:
        matrix = matrix.set_index('tax_current').T.to_dict('list')
        database = database.to_dict('records')
        mapped_database = map_and_concat(database, matrix)
        mapped_database = pd.DataFrame.from_dict(mapped_database)
        mapped_database.to_json(args.output, orient='records')
        return 0


if __name__ == "__main__":
    """ Run main method """
    sys.exit(main(sys.argv))
