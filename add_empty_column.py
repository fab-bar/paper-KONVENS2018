import argparse
import csv

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('--placeholder', default='--')
    args, _ = parser.parse_known_args()

    with open(args.infile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if not any(tok_line):
                print()
            else:
                print('\t'.join(tok_line + [args.placeholder]))
