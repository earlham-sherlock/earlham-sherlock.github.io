import pytest
import mock
import sherlock_ortholog_mapper


parameters = ["../example_files/human_to_mouse_orthology.tsv", 9606, "10090", "../example_files/test_output/"]
parameters2 = "10090, 7227"


@mock.patch.object(sherlock_ortholog_mapper, 'parse_args')
def test_input_not_file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', parameters[1], parameters[2], parameters[3]]
        sherlock_ortholog_mapper.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(sherlock_ortholog_mapper, 'parse_args')
def test_number_of_input_files_and_number_of_to_tax_ids(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = [parameters[0], parameters[1], parameters2, parameters[3]]
        sherlock_ortholog_mapper.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
