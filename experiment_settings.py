colnumbers = {
    'orig': 0,
    'simple': 1,
    'norm': 2,
    'pos': 3,
    'morph': 4,
    'lemma': 5,
    'autonorm_tok': 6,
    'autonorm_simpl': 7,
    'normpos': 8,
    'origpos': 9,
    'simplpos': 10,
    'autonorm_tok_pos': 11,
    'autonorm_simpl_pos': 12,
    'spellvar': 13,
    'posmorphvar': 14,
    'posvar': 15,
    'spellvarauto_exact': 16,
    'spellvarauto_norm': 17,
    'spellvarauto_pos': 18,
}

datasets = {
    'rem',
    'ren'
}

modelfolder = 'models'
predfolder = 'pred'
filenames = {
    'trainfile': 'data/{textname}_train',
    'testfile': 'data/{textname}_{testset}',
    'goldfile': 'data/{textname}_{testset}',
    'predfile': predfolder + '/{textname}_{experiment}_{testset}_pred.csv',
    'modelfile': modelfolder + '/{experiment}_{traintext}.model',
}

traincommands = {
    'marmot': 'java -Xmx5G -cp lib/cistern/marmot/marmot.jar marmot.morph.cmd.Trainer -train-file form-index={formindex},tag-index=' + str(colnumbers['pos']) + ',{trainfile} {options} --tag-morph False -model-file {modelfile}',
    'hunpos': 'sed \'1i123\t123\t123\t--\t--\t--\t--\' {trainfile} | cut -f{formindex},' + str(colnumbers['pos']+1) + ' | lib/hunpos/build/install/bin/hunpos-train {modelfile}',
    'rft': 'cut -f{formindex},' + str(colnumbers['pos']+1) + ' {trainfile} > {trainfile}.input; lib/RFTagger/bin/rft-train {trainfile}.input lib/RFTagger/wordclass/wordclass.txt {modelfile}; rm {trainfile}.input',
}

predictcommands = {
    'marmot': 'java -cp lib/cistern/marmot/marmot.jar marmot.morph.cmd.Annotator --model-file {modelfile} --test-file form-index={formindex},{testfile} --pred-file {predfile}',
    'hunpos': 'cut -f{formindex} {testfile} | lib/hunpos/build/install/bin/hunpos-tag {modelfile} > {predfile}',
    'rft': 'cut -f{formindex} {testfile} > {testfile}.input; lib/RFTagger/bin/rft-annotate {modelfile} {testfile}.input {predfile}; rm {testfile}.input',
}

def marmot_get_annotations(line):

    pos = line[5]
    return [line[1], pos]

def hunpos_get_annotations(line):

    pos = line[1]
    return [line[0], pos]

def rft_get_annotations(line):

    return [line[0], line[1]]


def marmot_experiment(formindex, options, formindex_test=None):

        if formindex_test is None:
            formindex_test = formindex

        return {
            'line_parser': marmot_get_annotations,
            'delimiter': '\t',
            'traincommand': traincommands['marmot'].format(formindex=formindex, options=options, trainfile='{trainfile}', modelfile='{modelfile}'),
            'predictcommand': predictcommands['marmot'].format(formindex=formindex_test, modelfile='{modelfile}', testfile='{testfile}', predfile='{predfile}')
        }


def marmot_hist_experiment(formindex, options, formindex_test=None):

    hist_options = '--rare-word-max-freq 30 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'

    if options:
        hist_options = ' '.join([options, hist_options])

    return marmot_experiment(formindex, hist_options, formindex_test)

experiments = {

    ##### Baselines

    'hunpos-orig': {
        'line_parser': hunpos_get_annotations,
        'delimiter': '\t',
        'traincommand': traincommands['hunpos'].format(formindex=str(colnumbers['orig']+1), trainfile='{trainfile}', modelfile='{modelfile}'),
        'predictcommand': predictcommands['hunpos'].format(formindex=str(colnumbers['orig']+1), modelfile='{modelfile}', testfile='{testfile}', predfile='{predfile}')
    },
    'rft-orig': {
        'line_parser': rft_get_annotations,
        'delimiter': '\t',
        'traincommand': traincommands['rft'].format(formindex=str(colnumbers['orig']+1), trainfile='{trainfile}', modelfile='{modelfile}'),
        'predictcommand': predictcommands['rft'].format(formindex=str(colnumbers['orig']+1), modelfile='{modelfile}', testfile='{testfile}', predfile='{predfile}')
    },
    'marmot-orig': marmot_experiment(str(colnumbers['orig']), ''),

    ##### Marmot - Affix length

    'marmot-affix16-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 16'),
    'marmot-affix13-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 13'),
    'marmot-affix7-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 7'),
    'marmot-affix4-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 4'),

    ##### Marmot - Affix length + Infix

    'marmot-infix-affix16-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 16 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix13-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 13 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix10-orig': marmot_experiment(str(colnumbers['orig']), '--feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix7-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 7 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-orig': marmot_experiment(str(colnumbers['orig']), '--max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),

    ##### Marmot - Affix length 4 + rare words

    'marmot-infix-affix4-rare5-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 5 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare15-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 15 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare20-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 20 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare25-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 25 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare30-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 30 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare35-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 35 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare40-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 40 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-raremax-orig': marmot_experiment(str(colnumbers['orig']), '--rare-word-max-freq 2147483647 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),

    ##### Simple

    'marmot-orig-simpl': marmot_experiment(str(colnumbers['simple']), ''),
    'marmot-hist-simpl': marmot_hist_experiment(str(colnumbers['simple']), ''),

    ##### Rare words

    'marmot-infix-affix4-rare5-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 5 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare10-simpl': marmot_experiment(str(colnumbers['simple']), '--max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare15-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 15 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare20-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 20 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare25-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 25 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare35-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 35 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-rare40-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 40 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),
    'marmot-infix-affix4-raremax-simpl': marmot_experiment(str(colnumbers['simple']), '--rare-word-max-freq 2147483647 --max-affix-length 4 --feature-templates form,rare,affix,infix,context,sig,bigrams'),

    #### ---- Norm

    'marmot-orig-norm': marmot_experiment(str(colnumbers['norm']), ''),
    'marmot-hist-norm': marmot_hist_experiment(str(colnumbers['norm']), ''),

    #### ---- Norm auto

    'marmot-orig-autonorm': marmot_experiment(str(colnumbers['norm']), '', str(colnumbers['autonorm_tok'])),
    'marmot-hist-autonorm': marmot_hist_experiment(str(colnumbers['norm']), '', str(colnumbers['autonorm_tok'])),

    ####  ----- Ext features

    'marmot-orig-normpos': marmot_experiment(str(colnumbers['orig']) + ',token-feature-index=' + str(colnumbers['normpos']), ''),
    'marmot-hist-normpos': marmot_hist_experiment(str(colnumbers['orig']) + ',token-feature-index=' + str(colnumbers['normpos']), ''),

    'marmot-orig-origpos': marmot_experiment(str(colnumbers['orig']) + ',token-feature-index=' + str(colnumbers['origpos']), ''),
    'marmot-hist-origpos': marmot_hist_experiment(str(colnumbers['orig']) + ',token-feature-index=' + str(colnumbers['origpos']), ''),

    'marmot-orig-normnormpos': marmot_experiment(str(colnumbers['norm']) + ',token-feature-index=' + str(colnumbers['normpos']), ''),
    'marmot-orig-autonormnormpos': marmot_experiment(str(colnumbers['norm']) + ',token-feature-index=' + str(colnumbers['normpos']), '', str(colnumbers['autonorm_tok']) + ',token-feature-index=' + str(colnumbers['normpos'])),


    ### Spellvar - Upper bounds


    'marmot-orig-spellvar': marmot_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvar'])),
    'marmot-hist-spellvar': marmot_hist_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvar'])),

    'marmot-orig-posvar': marmot_experiment(str(colnumbers['orig']), '', str(colnumbers['posvar'])),
    'marmot-hist-posvar': marmot_hist_experiment(str(colnumbers['orig']), '', str(colnumbers['posvar'])),

    ### Spellvar - Auto

    'marmot-orig-spellvarautoexact': marmot_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvarauto_exact'])),
    'marmot-hist-spellvarautoexact': marmot_hist_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvarauto_exact'])),

    'marmot-orig-spellvarautonorm': marmot_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvarauto_norm'])),
    'marmot-hist-spellvarautonorm': marmot_hist_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvarauto_norm'])),

    'marmot-orig-spellvarautopos': marmot_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvarauto_pos'])),
    'marmot-hist-spellvarautopos': marmot_hist_experiment(str(colnumbers['orig']), '', str(colnumbers['spellvarauto_pos'])),

    ### Embeddings

    'marmot-orig-embeddings-svd': marmot_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/svd/vectors.txt'),
    'marmot-hist-embeddings-svd': marmot_hist_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/svd/vectors.txt'),

    'marmot-orig-embeddings-sgns': marmot_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/sgns/vectors.txt'),
    'marmot-hist-embeddings-sgns': marmot_hist_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/sgns/vectors.txt'),

    'marmot-orig-embeddings-fasttext': marmot_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/fasttext/{traintext}.vec'),
    'marmot-hist-embeddings-fasttext': marmot_hist_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/fasttext/{traintext}.vec'),

    'marmot-orig-embeddings-svd-autospellvar': marmot_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/svd/vectors.txt', str(colnumbers['spellvarauto_exact'])),
    'marmot-hist-embeddings-svd-autospellvar': marmot_hist_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/svd/vectors.txt', str(colnumbers['spellvarauto_exact'])),

    'marmot-orig-embeddings-sgns-autospellvar': marmot_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/sgns/vectors.txt', str(colnumbers['spellvarauto_exact'])),
    'marmot-hist-embeddings-sgns-autospellvar': marmot_hist_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/sgns/vectors.txt', str(colnumbers['spellvarauto_exact'])),

    'marmot-orig-embeddings-fasttext-autospellvar': marmot_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/fasttext/{traintext}.vec', str(colnumbers['spellvarauto_exact'])),
    'marmot-hist-embeddings-fasttext-autospellvar': marmot_hist_experiment(str(colnumbers['orig']), '--type-embeddings dense=True,data/embeddings/{traintext}_background/fasttext/{traintext}.vec', str(colnumbers['spellvarauto_exact'])),

}
