import pytest
import mock
import os
import go_annotations_loader


parameters = ["example_files/test.gaf", 9606, "example_files/readme.md"]


@mock.patch.object(go_annotations_loader, 'parse_args')
def test_input_not_file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', parameters[1]]
        go_annotations_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(go_annotations_loader, 'parse_args')
def test_input_file_not_an_obo_file(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = [parameters[2], parameters[1]]
        go_annotations_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


@mock.patch.object(go_annotations_loader, 'parse_args')
def test_number_of_lines(args):
    args.return_value = [parameters[0], parameters[1]]
    go_annotations_loader.main()

    output_folder = parameters[0].split("/")[:-1]
    output_folder = "".join(output_folder)
    new_folder = os.path.join(output_folder, f'tax_id=9606')
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)

    output_file = os.path.join(new_folder, f'go_annotations.json')

    lines_in_output = sum(1 for line in open(output_file))

    assert lines_in_output == 19
