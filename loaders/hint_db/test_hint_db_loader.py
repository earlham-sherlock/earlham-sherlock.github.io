import pytest
import mock
import os
import hint_db_loader


parameters = ["example_files/test.tsv",
                      "uniprotac",
                      9606,
                      326,
                      "protein"]


@mock.patch.object(hint_db_loader, 'parse_args')
def test_input__file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', parameters[1], parameters[1], parameters[2], parameters[2], parameters[3],
                             parameters[3], parameters[4], parameters[4], False]
        hint_db_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(hint_db_loader, 'parse_args')
def test_number_of_lines(args):
    args.return_value = [parameters[0], parameters[1], parameters[1], parameters[2], parameters[2], parameters[3],
                         parameters[3], parameters[4], parameters[4], False]
    hint_db_loader.main()

    lines_in_input = sum(1 for line in open(parameters[0]))

    output_folder = parameters[0].split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'interactor_a_tax_id={9606}')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'hint_db.json')

    lines_in_output = sum(1 for line in open(output_file))

    assert lines_in_input - 1 == lines_in_output
