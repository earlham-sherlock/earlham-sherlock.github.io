import pytest
import mock
import os
import json
import mentha_db_loader


parameters = ["example_files/test.tsv", 9606, "23900247"]


@mock.patch.object(mentha_db_loader, 'parse_args')
def test_input__file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', "uniprotac", "uniprotac", parameters[1], 326, "protein", 326, "protein", False,
                             False, False, parameters[2]]

        mentha_db_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(mentha_db_loader, 'parse_args')
def test_number_of_lines(args):
    args.return_value = [parameters[0], "uniprotac", "uniprotac", parameters[1], 326, "protein", 326, "protein", False,
                         False, False, parameters[2]]

    mentha_db_loader.main()

    lines_in_input = sum(1 for line in open(parameters[0]))

    output_folder = parameters[0].split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id=9606')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'mentha_db.json')

    lines_in_output = sum(1 for line in open(output_file))

    assert lines_in_input == lines_in_output


@mock.patch.object(mentha_db_loader, 'parse_args')
def test_values_in_the_output(args):
    args.return_value = [parameters[0], "uniprotac", "uniprotac", parameters[1], 326, "protein", 326, "protein", False,
                         False, False, parameters[2]]

    mentha_db_loader.main()

    output_folder = parameters[0].split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id={9606}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'mentha_db.json')

    with open(output_file, 'r') as out:

        for line in out:
            json_line = json.loads(line.strip())

            assert json_line["interactor_a_id_type"] == "uniprotac"
            assert json_line["interactor_b_id_type"] == "uniprotac"
            assert json_line["interactor_a_molecule_type_mi_id"] == 326
            assert json_line["interactor_b_molecule_type_mi_id"] == 326
            assert json_line["interactor_a_molecule_type_name"] == "protein"
            assert json_line["interactor_b_molecule_type_name"] == "protein"
            assert json_line["interaction_detection_methods_mi_id"] != []
            assert json_line["interaction_types_mi_id"] != []
            assert json_line["source_database_mi_id"] != []
            assert 23900247 in json_line["pmids"]
