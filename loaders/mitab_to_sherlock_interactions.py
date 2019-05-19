import argparse
import sys
sys.path.append("..")
import mitab_handler

class ArgumentParser:

    def __init__(self, args=None):
        parser = argparse.ArgumentParser(description="This tool will take a single MITAB file and converts it to a sherlock "
                                                     "json interaction file. It will not change the order of "\
                                                     "interactions, nor will remove duplicate links.")

        parser.add_argument("-i", "--input-file",
                            help="path to single MITAB file",
                            dest="input_file",
                            action="store",
                            required=True)

        parser.add_argument("-o", "--output-file",
                            help="path to sherlock interaction json file",
                            dest="output_file",
                            action="store",
                            required=True)

        results = parser.parse_args(args)

        self.out_file = results.output_file.strip()
        self.in_file = results.input_file.strip()


if __name__ == "__main__":
    params = ArgumentParser(sys.argv[1:])

    mitab = mitab_handler.MiTabHandler()
    mitab.parse_mitab(params.in_file)
    mitab.serialise_sherlock(params.out_file)
