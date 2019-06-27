import pytest
import mock
import os
import json
import snp_db_loader


parameters = ["example_files/test.vcf", "example_files/dbsnp/", "example_files/test2.tsv"]


@mock.patch.object(snp_db_loader, 'parse_args')
def test_input_file_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', parameters[1]]
        snp_db_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(snp_db_loader, 'parse_args')
def test_input_file_is_not_vcf_file(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = [parameters[2], parameters[1]]
        snp_db_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


@mock.patch.object(snp_db_loader, 'parse_args')
def test_output_folder_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = [parameters[0], "output_folder"]
        snp_db_loader.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3
