import os
import os.path

import experiment_settings

try:
        os.mkdir(experiment_settings.modelfolder)
except:
        pass
try:
        os.mkdir(experiment_settings.predfolder)
except:
        pass

for experimentname, experiment in experiment_settings.experiments.items():

        ## tag based on groups
        for group in experiment_settings.datasets:

            if not os.path.isfile(experiment_settings.filenames['modelfile'].format(experiment=experimentname, traintext=group)):
                    os.system(experiment['traincommand'].format(
                            trainfile=experiment_settings.filenames['trainfile'].format(textname=group),
                            modelfile=experiment_settings.filenames['modelfile'].format(experiment=experimentname, traintext=group),
                            traintext=group))

            for testset in ["devel", "test"]:
                    if not os.path.isfile(experiment_settings.filenames['predfile'].format(experiment=experimentname, textname=group, testset=testset)):
                            os.system(experiment['predictcommand'].format(
                                    modelfile=experiment_settings.filenames['modelfile'].format(experiment=experimentname, traintext=group),
                                    testfile=experiment_settings.filenames['testfile'].format(textname=group, testset=testset),
                                    predfile=experiment_settings.filenames['predfile'].format(experiment=experimentname, textname=group, testset=testset)))
