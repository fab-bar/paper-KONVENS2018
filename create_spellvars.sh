function create_spellvar() {

    python3 extract_data_for_spellvardetection.py data/${1}_train data/${1}_devel data/${1}_test $3 $4 $5 data/${1}_trainspellvars_${2} data/${1}_traintoken_${2} data/${1}_traindict_${2} data/${1}_develdict_${2} data/${1}_testdict_${2}

    source lib/SpellvarDetection/.venv/bin/activate
    lib/SpellvarDetection/bin/generate_candidates data/${1}_traindict_${2} levenshtein '{"max_dist": 1, "dictionary": "data/'${1}'_traindict_'${2}'"}' data/${1}_traincandidates_${2}
    lib/SpellvarDetection/bin/generate_candidates data/${1}_develdict_${2} levenshtein '{"max_dist": 1, "dictionary": "data/'${1}'_traindict_'${2}'"}' data/${1}_develcandidates_${2}
    lib/SpellvarDetection/bin/generate_candidates data/${1}_testdict_${2} levenshtein '{"max_dist": 1, "dictionary": "data/'${1}'_traindict_'${2}'"}' data/${1}_testcandidates_${2}


    lib/SpellvarDetection/bin/extract_positive_and_negative_pairs data/${1}_trainspellvars_${2} data/${1}_traincandidates_${2} data/${1}_traintoken_${2} 0 data/${1}_trainspellvar_${2}_positive data/${1}_trainspellvar_${2}_negative

    lib/SpellvarDetection/bin/train_filter __bagging_svm__ '[{"type": "surface", "name": "surface", "key": "alignment_ngrams"}]' data/spellvar_model/${1}_${2} data/${1}_trainspellvar_${2}_positive data/${1}_trainspellvar_${2}_negative
    lib/SpellvarDetection/bin/filter data/${1}_develcandidates_${2} data/spellvar_model/${1}_${2} data/${1}_devel_spellvars_${2}
    lib/SpellvarDetection/bin/filter data/${1}_testcandidates_${2} data/spellvar_model/${1}_${2} data/${1}_test_spellvars_${2}
    deactivate

    rm data/${1}_traintoken_${2} data/${1}_traindict_${2} data/${1}_develdict_${2} data/${1}_testdict_${2} \
       data/${1}_trainspellvars_${2} data/${1}_traincandidates_${2} data/${1}_develcandidates_${2} data/${1}_testcandidates_${2} \
       data/${1}_trainspellvar_${2}_positive data/${1}_trainspellvar_${2}_negative

}

mkdir -p data/spellvar_model

create_spellvar rem exact 1 4 6
create_spellvar rem exactnorm 1 3 3
create_spellvar rem pos 1 4 4

create_spellvar ren exact 1 4 6
create_spellvar ren pos 1 4 4

