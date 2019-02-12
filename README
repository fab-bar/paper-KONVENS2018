# POS tagging texts with spelling variation

Scripts to run POS tagging experiments with historical German texts that contain spelling variants.
The scripts can be used to reproduce the experiments from the following paper:

```bib
@inproceedings{Barteld-et-al-2018,
  author    = {Fabian Barteld and Chris Biemann and Heike Zinsmeister},
  editor    = {Adrien Barbaresi and Hanno Biber and Friedrich Neubarth and Rainer Osswald},
  title     = {Variations on the theme of variation: Dealing with spelling variation for finegrained {POS} tagging of historical texts},
  booktitle = {Proceedings of the 14th Conference on Natural Language Processing, {KONVENS} 2018, Vienna, Austria, September 19-21, 2018},
  pages     = {202--212},
  publisher = {{\"{O}}sterreichische Akademie der Wissenschaften},
  year      = {2018},
  url       = {https://www.oeaw.ac.at/fileadmin/subsites/academiaecorpora/PDF/konvens18\_23.pdf},
}
```

## Install dependencies

Script to install the tools needed for the experiments.
For tools under version control, the version used for the experiments in the paper is checked out.

- install_dependencies.sh:
  Download and build the following tools in the folder lib/

  - SpellvarDetection (https://github.com/fab-bar/spellvardetection)
  - csmtiser (https://github.com/clarinsi/csmtiser)
  - hyperwords (https://bitbucket.org/omerlevy/hyperwords)
  - fastText (https://github.com/facebookresearch/fastText)
  - TreeTagger (https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)
  - RFTagger (https://www.cis.uni-muenchen.de/~schmid/tools/RFTagger/)
  - HunPos (https://github.com/mivoq/hunpos)
  - Marmot (http://cistern.cis.lmu.de/marmot/)


## Data

Scripts to get and prepare the data used for the POS tagging experiments.

- prepare_re[mn].sh:
  Download and prepare the data from ReM/ReN.
  Data is split in train, test, devel and background corpus (for creation of embeddings)

  - ReM is version 1.0 (islrn.org/resources/332-536-136-099-5)
  - ReN is version 0.6 (http://hdl.handle.net/11022/0000-0007-C64C-5)

Run prepare_re[mn].sh to extract the data and remove texts not used for the experiments.

- create_embeddings.sh
- create_normalization.sh
- create_spellvars.sh

Run the create_* scripts to create the embeddings, automatic normalizations and automatically detected spelling variants for ReM and ReN that are used in the experiments.

- add_features_re[mn].sh

Run add_features_re[mn].sh to add additional features to the data files.

After successfully running all of the above mentioned scripts, the data folder contains the files
re[mn]_train, re[mn]_devel and re[mn]_test. These files contain the follwing columns:

01. Token - Strict
02. Token - Simple 
03. Normalization (only ReM)
04. POS
05. Morph
06. Lemma
07. csmtiser - Normalization based on strict (only ReM)
08. csmtiser - Normalization based on simple (only ReM)
09. TreeTagger - POS tag based on strict (only ReM)
10. TreeTagger - POS tag based on simple (only ReM)
11. TreeTagger - POS tag based on norm (only ReM)
12. TreeTagger - POS tag based on csmtiser normlization strict (only ReM)
13. TreeTagger - POS tag based on csmtiser normalization simple (only ReM)

only devel and test:

14. Gold spelling variant
15. Gold spelling variant approximated with pos and morph
16. Gold spelling variant approximated with pos
17. Generated spelling variant based on pos, morph and lemma
18. Generated spelling variant based on norm (only ReM)
19. Generated spelling variant based on pos

## Running the experiments

The experiments are defined in `experiment_settings.py`. After having
succesfully installed the dependencies and prepared the data, they can be run
with the scripts `train_and_annotate.py`.

There are two scripts to show the results of the experiments:

- eval.py
  Output the results of all experiments for the given data- and testset.  
  Usage: `python3 eval.py dataset testset`

- compare.py
  Compare two experiments using McNemar's test with continuity correction.  
  Usage: `python3 compare.py dataset testset experiment-1-name experiment-2-name`