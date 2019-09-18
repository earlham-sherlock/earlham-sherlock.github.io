import pytest
import mock
import sherlock_table_loader


parameters = ["example_files/test.tsv", "test", "example_files/output.json"]
parameters2 = ["example_files/test_file.tsv", "test", "example_files/output.json"]
parameters3 = ["example_files/test_file2.tsv", "test", "example_files/output.json"]


@mock.patch.object(sherlock_table_loader, 'parse_args')
def test_input_not_file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', parameters[1], parameters[2]]
        sherlock_table_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(sherlock_table_loader, 'parse_args')
def test_first_line_contains_special_character(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = [parameters2[0], parameters2[1], parameters2[2]]
        sherlock_table_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


@mock.patch.object(sherlock_table_loader, 'parse_args')
def test_type_is_incorrect(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = [parameters3[0], parameters3[1], parameters3[2]]
        sherlock_table_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3


@mock.patch.object(sherlock_table_loader, 'parse_args')
def test_number_of_lines(args):
    args.return_value = [parameters[0], parameters[1], parameters[2]]
    sherlock_table_loader.main()

    lines_in_input = sum(1 for line in open(parameters[0])) - 2
    lines_in_output = sum(1 for line in open(parameters[2]))

    assert lines_in_input == lines_in_output
