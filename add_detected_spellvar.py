import argparse
from collections import defaultdict
import csv
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('trainfile')
    parser.add_argument('testfile')
    parser.add_argument('spellvarfile')
    parser.add_argument('tok_column', type=int)
    args, _ = parser.parse_known_args()

    spellvars = json.load(open(args.spellvarfile))
    known_types = defaultdict(int)

    with open(args.trainfile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if tok_line:
                known_types[tok_line[args.tok_column -1]] += 1

    with open(args.testfile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if tok_line:
                if (tok_line[args.tok_column-1] not in known_types.keys()):
                    curr_spellvars = spellvars[tok_line[args.tok_column-1]]
                    if curr_spellvars:
                        ## get most frequent spellvar
                        spellvar_freq= {spellvar: known_types[spellvar] for spellvar in curr_spellvars}
                        spellvar = sorted(spellvar_freq, key=spellvar_freq.get)[-1]
                    else: ## fall back to type
                        spellvar = tok_line[args.tok_column-1]

                    print('\t'.join(tok_line + [spellvar]))
                else:
                    print('\t'.join(tok_line + [tok_line[args.tok_column-1]]))
            else:
                print()
