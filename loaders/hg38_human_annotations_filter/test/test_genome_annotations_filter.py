import pytest
import genome_annotations_filter
import mock
import os


reference_annotation_bed_file = ["example_files/test_reference_file.bed"]


@mock.patch.object(genome_annotations_filter, 'parse_args')
def test_reference_bed_file_exists(args, tmpdir):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = ['file', 'gene', 'ensembl', False, 'hg38', tmpdir]
        genome_annotations_filter.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@mock.patch.object(genome_annotations_filter, 'parse_args')
def test_reference_bed_file_is_a_bed_file(args, tmpdir):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fake_file = tmpdir.join("wrong_file.tsv")
        fake_file.write("")
        args.return_value = [str(fake_file), 'gene', 'ensembl', False, 'hg38', tmpdir]
        genome_annotations_filter.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


@mock.patch.object(genome_annotations_filter, 'parse_args')
def test_output_folder_exists(args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        args.return_value = args.return_value = [reference_annotation_bed_file[0], 'gene', 'ensembl', False, 'hg38', 'output']
        genome_annotations_filter.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3


@mock.patch.object(genome_annotations_filter, 'parse_args')
def test_entity_type_exists(args, tmpdir):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        output_folder = tmpdir.mkdir('output')
        args.return_value = args.return_value = [reference_annotation_bed_file[0], 'asdasd', 'ensembl', False, 'hg38', output_folder]
        genome_annotations_filter.main()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 4


@mock.patch.object(genome_annotations_filter, 'parse_args')
def test_case_one(args, tmpdir):
    output_folder = tmpdir.mkdir('output')
    args.return_value = [reference_annotation_bed_file[0], 'exon', 'ensembl', 'ucsc', 'hg38', output_folder]
    genome_annotations_filter.main()

    assert len([name for name in os.listdir(output_folder)]) == 3

    chromosome_1_json = os.path.join(output_folder, "chr=chr1", "exon.json")
    num_lines = sum(1 for line in open(chromosome_1_json))
    exon_number_chr1 = 5
    assert num_lines == exon_number_chr1

    chromosome_5_json = os.path.join(output_folder, "chr=chr5", "exon.json")
    num_lines = sum(1 for line in open(chromosome_5_json))
    exon_number_chr5 = 2
    assert num_lines == exon_number_chr5

    chromosome_11_json = os.path.join(output_folder, "chr=chr11", "exon.json")
    num_lines = sum(1 for line in open(chromosome_11_json))
    exon_number_chr11 = 1
    assert num_lines == exon_number_chr11


@mock.patch.object(genome_annotations_filter, 'parse_args')
def test_case_two(args, tmpdir):
    output_folder = tmpdir.mkdir('output')
    args.return_value = [reference_annotation_bed_file[0], 'intron', 'ensembl', 'ucsc', 'hg38', output_folder]
    genome_annotations_filter.main()

    assert len([name for name in os.listdir(output_folder)]) == 3

    chromosome_1_json = os.path.join(output_folder, "chr=chr1", "intron.json")
    num_lines = sum(1 for line in open(chromosome_1_json))
    exon_number_chr1 = 5
    assert num_lines == exon_number_chr1 - 1

    chromosome_5_json = os.path.join(output_folder, "chr=chr5", "intron.json")
    num_lines = sum(1 for line in open(chromosome_5_json))
    exon_number_chr5 = 2
    assert num_lines == exon_number_chr5 - 1

    chromosome_11_json = os.path.join(output_folder, "chr=chr11", "intron.json")
    num_lines = sum(1 for line in open(chromosome_11_json))
    exon_number_chr11 = 1
    assert num_lines == exon_number_chr11 - 1
