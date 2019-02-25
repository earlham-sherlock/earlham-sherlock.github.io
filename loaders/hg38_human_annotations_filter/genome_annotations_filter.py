import argparse
import os
import sys
import json


def parse_args(args):
    help_text = \
        """
        === Genome Annotations Filter script ===
        """

    parser = argparse.ArgumentParser(description=help_text)

    # A reference .bed annotation file
    parser.add_argument("-r", "--reference-annotation-bed-file",
                        help="<path to a reference annotation .bed file> [mandatory]",
                        type=str,
                        dest="reference_annotation_file",
                        action="store",
                        required=True)

    # Entity type
    parser.add_argument("-et", "--entity-type",
                        help="<MI term name entity type> [mandatory]",
                        type=str,
                        dest="entity_type",
                        action="store",
                        required=True)

    # Entity id type
    parser.add_argument("-eit", "--entity-id-type",
                        help="<UniProtKB DBref entity id type> [mandatory]",
                        type=str,
                        dest="entity_id_type",
                        action="store",
                        required=True)

    # Source DB
    parser.add_argument("-db", "--source-db",
                        help="<optional text field (can be null, but can not be empty string), contains the name / "
                             "version of the database or the experiment ID> [mandatory]",
                        type=str,
                        dest="source_db",
                        action="store",
                        required=False,
                        default=None)

    # Genome
    parser.add_argument("-g", "--genome",
                        help="<genome version> [mandatory]",
                        type=str,
                        dest="genome",
                        action="store",
                        required=True)

    # Output file path
    parser.add_argument("-o", "--output-folder",
                        help="<path to an output folder> [mandatory]",
                        type=str,
                        dest="output_folder",
                        action="store",
                        required=True)

    results = parser.parse_args(args)
    return results.reference_annotation_file, results.entity_type.lower(), results.entity_id_type.lower(), \
           results.source_db, results.genome.lower(), results.output_folder


def progress_bar(iteration, total, barLength):
   percent = int((iteration / total) * 100)
   bar_fill = '=' * percent
   bar_empty = ' ' * (barLength - percent)
   actual = bar_fill + bar_empty
   sys.stdout.write(f'\r[{actual}] {percent}% done')


def check_params(reference_annotation_file, output_folder):

    if not os.path.isfile(reference_annotation_file):
        sys.stderr.write(f"ERROR! the specified reference annotation .bed file doesn't exists: "
                         f"{reference_annotation_file}")
        sys.exit(1)

    if not reference_annotation_file.endswith(".bed"):
        sys.stderr.write(f"ERROR! the specified reference annotation file is not a .bed file: "
                         f"{reference_annotation_file}")
        sys.exit(2)

    if not os.path.isdir(output_folder):
        sys.stderr.write(f"ERROR! the specified output folder doesn't exists: {output_folder}")
        sys.exit(3)


def write_to_json(entity_type, entity_id_type, entity_id, start, end, strand, source_db, genome, output):

        json_dictionary = {}
        json_dictionary["entity_type"] = entity_type
        json_dictionary["entity_id_type"] = entity_id_type
        json_dictionary["entity_id"] = entity_id
        json_dictionary["start"] = start
        json_dictionary["end"] = end
        if strand == "+" or strand == "-":
            json_dictionary["strand"] = strand
        else:
            json_dictionary["strand"] = None
        json_dictionary["source_db"] = source_db
        json_dictionary["genome"] = genome

        output.write(json.dumps(json_dictionary) + '\n')


def get_genes(line, entity_type, entity_id_type, source_db, genome, output):

    entity_id = line[3].lower()
    start = int(line[1])
    end = int(line[2])
    strand = line[5]
    write_to_json(entity_type, entity_id_type, entity_id, start, end, strand, source_db, genome, output)


def get_exons(line, entity_type, entity_id_type, source_db, genome, output):

    entity_id = line[3].lower()
    strand = line[5]

    exon_count = int(line[9])
    gene_start = int(line[1])
    if exon_count > 0:
        exon_starts = line[11].split(",")[:-1]
        exon_lengths = line[10].split(",")[:-1]
        for index in range(0, exon_count, 1):
            start = gene_start + int(exon_starts[index])
            end = start + int(exon_lengths[index])
            write_to_json(entity_type, entity_id_type, entity_id, start, end, strand, source_db, genome, output)


def get_introns(line, entity_type, entity_id_type, source_db, genome, output):

    entity_id = line[3].lower()
    strand = line[5]

    exon_count = int(line[9])
    gene_start = int(line[1])
    if exon_count > 0:
        exon_starts = line[11].split(",")[:-1]
        exon_lengths = line[10].split(",")[:-1]
        for index in range(0, exon_count - 1, 1):
            start = gene_start + int(exon_starts[index]) + int(exon_lengths[index])
            end = gene_start + int(exon_starts[index + 1])
            write_to_json(entity_type, entity_id_type, entity_id, start, end, strand, source_db, genome, output)


def get_mirnas(line, entity_type, entity_id_type, source_db, genome, output):

    entity_id = line[3].lower()
    start = int(line[1])
    end = int(line[2])
    strand = line[5]
    write_to_json(entity_type, entity_id_type, entity_id, start, end, strand, source_db, genome, output)


def main():

    reference_annotation_file, entity_type, entity_id_type, source_db, genome, output_folder = parse_args(sys.argv[1:])

    check_params(reference_annotation_file, output_folder)
    print(f'====== Parameters are fine, starting... ======')

    length = sum(1 for line in open(reference_annotation_file))

    if source_db:
        source_db = source_db.lower()

    entity_types = ["gene", "exon", "intron", "micro rna"]
    if entity_type not in entity_types:
        sys.stderr.write(f"ERROR! with this entity type: {entity_type}, the script can not handle with! "
                         f"Please choose an other entity type!")
        sys.exit(4)

    with open(reference_annotation_file, 'r') as reference:
        reference.readline()
        index = 1
        for line in reference:
            line = line.strip().split('\t')
            chromosome = line[0]
            new_folder = os.path.join(output_folder, f'chr={chromosome}')
            if not os.path.isdir(new_folder):
                os.mkdir(new_folder)

            if entity_type == "gene":
                json_file = os.path.join(new_folder, f'gene.json')
                with open(json_file, "a") as output:
                    get_genes(line, entity_type, entity_id_type, source_db, genome, output)

            if entity_type == "exon":
                json_file = os.path.join(new_folder, f'exon.json')
                with open(json_file, "a") as output:
                    new_entity_type = "gene"
                    get_exons(line, new_entity_type, entity_id_type, source_db, genome, output)

            if entity_type == "intron":
                json_file = os.path.join(new_folder, f'intron.json')
                with open(json_file, "a") as output:
                    new_entity_type = "gene"
                    get_introns(line, new_entity_type, entity_id_type, source_db, genome, output)

            if entity_type == "micro rna":
                json_file = os.path.join(new_folder, f'mirna.json')
                with open(json_file, "a") as output:
                    get_mirnas(line, entity_type, entity_id_type, source_db, genome, output)

            progress_bar(index, length, 100)
            index = index + 1

    progress_bar(length, length, 100)
    print(f'\n====== Genome Annotations script finished successfully! ======')


if __name__ == "__main__":
    main()
