import argparse
import tempfile
import sys
sys.path.append("..")
import mitab_handler

class ArgumentParser:

    def __init__(self, args=None):
        parser = argparse.ArgumentParser(description="This tool will take a set of sherlock json interaction files and produce "
                                                     "a single MITAB file. It will not change the order of interactions, nor will "
                                                     "remove duplicate links.")

        parser.add_argument("-i", "--input-files",
                            help="path to sherlock interaction json files, separated by comma",
                            dest="input_files",
                            action="store",
                            required=True)

        parser.add_argument("-o", "--output-file",
                            help="path to single MITAB file",
                            dest="output_file",
                            action="store",
                            required=True)

        results = parser.parse_args(args)

        self.in_files = list(map(lambda x: x.strip(), results.input_files.split(',')))
        self.out_file = results.output_file.strip()


if __name__ == "__main__":
    params = ArgumentParser(sys.argv[1:])

    temp_output_files = []

    for input_file in params.in_files:
        out_file = tempfile.NamedTemporaryFile()
        temp_output_files.append(out_file.name)
        print(f"processing {input_file} --> {out_file.name}")
        mitab = mitab_handler.MiTabHandler()
        mitab.parse_sherlock(input_file)
        mitab.serialise_mitab(out_file.name)

    with open(params.out_file, "w") as merged_output_file:
        for temp_file_name in temp_output_files:
            print(f"merging {temp_file_name} --> {params.out_file}")
            with open(temp_file_name) as temp_file:
                for line in temp_file:
                    merged_output_file.write(line)
