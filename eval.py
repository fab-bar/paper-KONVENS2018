import argparse
import csv
import statistics

from collections import Counter
from functools import reduce

import experiment_settings

def eval(gold_data, pred_data):

    correct_pos = 0
    number_tokens = 0

    for sentence_gold, sentence_pred in zip(gold_data, pred_data):
        for token_gold, token_pred in zip(sentence_gold, sentence_pred):
            number_tokens += 1

            ## remove morphological information
            poscomplete_gold = token_gold[1].split(".", 2)[0]
            poscomplete_pred = token_pred[1].split(".", 2)[0]

            if token_gold[1] == token_pred[1]:
                correct_pos += 1
            elif poscomplete_gold == poscomplete_pred:
                correct_pos += 1

    return correct_pos/number_tokens

def get_tagging_predictions(experiment, traintext, testtext, testset):

    tagger_data = []
    with open(experiment_settings.filenames['predfile'].format(textname=testtext, trainname=traintext, experiment=experiment, testset=testset), 'r', newline='') as csv_file:

        reader = csv.reader(csv_file, delimiter=experiment_settings.experiments[experiment]['delimiter'])

        curr_sent = []
        for line in reader:
            if line:
                curr_sent.append(experiment_settings.experiments[experiment]['line_parser'](line))
            else:
                tagger_data.append(curr_sent)
                curr_sent = []

    return tagger_data

def get_tagging_results(experiment, traintext, testtext, testset):

    return eval(gold_data, get_tagging_predictions(experiment, traintext, testtext, testset))

def output_results(results):

    for t, acc in sorted(results.items(), key=lambda item: item[1], reverse=True):
        print("{:50.50}: {:.2f}".format(t, acc*100))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    parser.add_argument('testset')
    args, _ = parser.parse_known_args()

    pos_accuracies = {}

    gold_data = []
    with open(experiment_settings.filenames['goldfile'].format(textname=args.dataset, testset=args.testset), 'r', newline='') as goldfilehandle:

        reader = csv.reader(goldfilehandle, delimiter='\t')

        curr_sent = []
        for line in reader:
            # if line: ## when pasting norm results, empty line contain tab
            if any(line):
                curr_sent.append([line[0], line[3]])
            else:
                gold_data.append(curr_sent)
                curr_sent = []

    for experimentname in experiment_settings.experiments.keys():

        result = get_tagging_results(experimentname, args.dataset, args.dataset, args.testset)

        pos_accuracies[experimentname] = result

    print("POS (Beleg<Lemma) accuracies:")
    output_results(pos_accuracies)
