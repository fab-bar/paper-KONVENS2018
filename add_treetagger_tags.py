import argparse
import csv

import treetaggerwrapper

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('tok_column', type=int)
    parser.add_argument('taggerdir')
    parser.add_argument('taggerparfile')
    args, _ = parser.parse_known_args()

    tagger = treetaggerwrapper.TreeTagger(TAGDIR=args.taggerdir, TAGPARFILE=args.taggerparfile)

    curr_sent = []

    with open(args.infile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if not any(tok_line):
                pos_tags = [tag.pos for tag in treetaggerwrapper.make_tags(tagger.tag_text([tok[args.tok_column - 1] for tok in curr_sent], tagonly=True))]
                curr_sent = [token + [pos] for token, pos in zip(curr_sent, pos_tags)]

                print('\n'.join(['\t'.join(tok) for tok in curr_sent]))
                print()
                curr_sent = []
            else:
                curr_sent.append(tok_line)


    ## assure that not missing any tags
    if curr_sent:
        print('No empty line at end of file')
