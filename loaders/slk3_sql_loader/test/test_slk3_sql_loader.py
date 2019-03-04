import pytest
import mock
import os
import slk3_sql_loader
import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)

    return None


parameters = ["example_files/test.db",
              250,
              "protein",
              250,
              "protein",
              469,
              "example_files/results.json"]


@mock.patch.object(slk3_sql_loader, 'parse_args')
def test_input_slk3_db_file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6]]
        slk3_sql_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(slk3_sql_loader, 'parse_args')
def test_reference_bed_file_is_a_bed_file(args, tmpdir):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fake_file = tmpdir.join("wrong_file.tsv")
        fake_file.write("")
        args.return_value = [str(fake_file), parameters[1], parameters[2], parameters[3], parameters[4], parameters[5], parameters[6]]
        slk3_sql_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


@mock.patch.object(slk3_sql_loader, 'parse_args')
def test_case_one(args):
    args.return_value = [parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5],
                         parameters[6]]
    slk3_sql_loader.main()

    connection = create_connection(parameters[0])
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT a.name AS a_name, b.name AS b_name, a.tax_id AS a_taxid, b.tax_id AS b_taxid, interaction_detection_method, interaction_types, publication_ids FROM edge LEFT JOIN node a ON edge.interactor_a_node_id = a.id LEFT JOIN node b ON edge.interactor_b_node_id = b.id;")

        lines = cur.fetchall()
        lenght = len(lines)

        num_lines = sum(1 for line in open(parameters[6]))

        assert num_lines == lenght


@mock.patch.object(slk3_sql_loader, 'parse_args')
def test_case_two(args):
    args.return_value = [parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5],
                         parameters[6]]
    slk3_sql_loader.main()

    connection = create_connection(parameters[0])
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT a.name AS a_name, b.name AS b_name, a.tax_id AS a_taxid, b.tax_id AS b_taxid, interaction_detection_method, interaction_types, publication_ids FROM edge LEFT JOIN node a ON edge.interactor_a_node_id = a.id LEFT JOIN node b ON edge.interactor_b_node_id = b.id;")

        taxid_9606 = 0
        taxid_7227 = 0
        lines = cur.fetchall()
        for line in lines:
            taxid = [item for item in line if item == "taxid:9606"]
            if taxid != []:
                taxid_9606 = taxid_9606 + 1
            taxid2 = [item for item in line if item == "taxid:7227"]
            if taxid2 != []:
                taxid_7227 = taxid_7227 + 1

        output_json = parameters[6]

        taxid_9606_output = 0
        taxid_7227_output = 0
        with open(output_json) as output:
            for line in output:
                taxid = line.find('9606')
                if taxid != -1:
                    taxid_9606_output = taxid_9606_output + 1
                taxid2 = line.find('7227')
                if taxid2 != -1:
                    taxid_7227_output = taxid_7227_output + 1

        assert taxid_9606 == taxid_9606_output
        assert taxid_7227 == taxid_7227_output


@mock.patch.object(slk3_sql_loader, 'parse_args')
def test_case_three(args):
    args.return_value = [parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5],
                         parameters[6]]
    slk3_sql_loader.main()

    output_json = parameters[6]
    with open(output_json) as output:
        for line in output:
            line = line.strip().split(":")
            assert len(line) == 15
