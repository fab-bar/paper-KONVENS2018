import abc
import argparse
import os
import re
import xml.etree.ElementTree as ET

class AnnoToken(metaclass=abc.ABCMeta):

    def __init__(self, xml_element):
        self._xml_element = xml_element

    def get_element_name():
        """class method that returns the xml element name"""
        return 'mod'

    def _get_annotation(self, annotation, default='--'):

        anno_node = self._xml_element.find(annotation)
        if anno_node is not None:
            return anno_node.attrib['tag']
        else:
            return default

    def getTrans(self):
        return self._xml_element.attrib['trans'].lower()

    def getSimple(self):
        return self._xml_element.attrib['ascii'].lower()

    def getUTF(self):
        return self._xml_element.attrib['utf'].lower()

    def getPOS(self):
        return self._get_annotation('pos') + '<' + self._get_annotation('pos_gen')

    @abc.abstractmethod
    def getMSD(self):
        pass

    @abc.abstractmethod
    def getLemma(self):
        pass

    @abc.abstractmethod
    def getNorm(self):
        pass


class REMAnnoToken(AnnoToken):

    def get_element_name():
        return 'tok_anno'

    def getMSD(self):

        return '.'.join([self._get_annotation('infl'), self._get_annotation('inflClass'), self._get_annotation('inflClass_gen')])

    def getLemma(self):

        return self._get_annotation('lemma') + '<' + self._get_annotation('lemma_gen')

    def getNorm(self):
        return self._get_annotation('norm', self.getSimple()).lower()

    def getBoundSent(self):

        return self._get_annotation('punc')

class RENAnnoToken(AnnoToken):

    def get_element_name():
        return 'anno'

    def getSimple(self):

        text = super().getSimple()
        ### create simplified form using the rules from Koleva et al. 2017 (https://doi.org/10.1075/ijcl.22.1.05kol)
        ### code has been provided by Melissa Farasyn
        rule1 = re.sub('c[k]?(?!h)', 'k', text)
        rule2 = re.sub('lyk', 'lik', rule1)
        rule3 = re.sub('lych', 'lich', rule2)
        rule4 = re.sub('lig', 'lyg', rule3)
        rule5 = re.sub('th(?!e[iye]?t|aft|alv|ert)', 't', rule4)
        rule6 = re.sub(r'\b.f[f]?te\b', 'efte', rule5)
        rule7 = re.sub('(?<![ng])g(?![ght])', 'gh', rule6)
        rule8 = re.sub('ggh(?!t)', 'gh', rule7)
        rule9 = re.sub('(?<!n)g[h]?t', 'cht', rule8)
        rule10 = re.sub('[aA][iye]', 'a', rule9)
        rule11 = re.sub('(?<!gh)ei', 'ey', rule10)
        rule12 = re.sub('(?<!gh)(?<!b)ee', 'ey', rule11)
        rule13 = re.sub('iy', 'i', rule12)
        rule14 = re.sub('(?<![xi])ij', 'i', rule13)
        rule15 = re.sub('o[ei]', 'oy', rule14)
        rule16 = re.sub(r'\beyne(?=\b)', 'ene', rule15)
        rule17 = re.sub(r'\beyne(?=[nrm]e\b)', 'ene', rule16)
        rule18 = re.sub(r'\beyne(?=[nrms]\b)', 'ene', rule17)
        rule19 = re.sub(r'(?<![AaEeIiUuOoYy])y(?![aeiuoyg])', 'i', rule18)
        rule20 = re.sub(r'(?<!\b)dt(?=\b)', 't', rule19)
        rule21 = re.sub(r'(?<!\b.n)(?<!\b)d(?![AaEeIiUuOo])(?=\b)', 't', rule20)
        rule22 = re.sub(r'ou[uv]', 'ouw', rule21)
        rule23 = re.sub('uul', 'vul', rule22)
        rule24 = re.sub(r'\bu[v]', 'vu', rule23)
        rule25 = re.sub(r'(?<=[AaEeIiUuOo])v(?=[AaEeIiUuOo])', 'u', rule24)
        return re.sub(r'(?<=\b).nd[e]?(?=\b)', 'vnde', rule25)

    def getMSD(self):

        return self._get_annotation('morph')

    def getLemma(self):

        return self._get_annotation('lemma_wsd')

    def getNorm(self):

        ## REN does not have normalization
        return "--"


    def getBoundSent(self):

        return self._get_annotation('bound_sent')

anno_token_types = {
    'rem': REMAnnoToken,
    'ren': RENAnnoToken
}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('corpus_folder',
                        help='Folder with CoraXML files')
    parser.add_argument('corpus_type', choices=anno_token_types.keys(),
                        help='The CoraXML dialect')
    parser.add_argument('corpus_name',
                        help='Name of the corpus - will be used for output filenames')
    parser.add_argument('--nosplit', action='store_true', default=False)
    parser.add_argument('--trainsize', default=2000)
    parser.add_argument('--develsize', default=1000)
    parser.add_argument('--testsize', default=1000)
    parser.add_argument('--outfolder', help='Add the corpus files to the given folder')
    args, _ = parser.parse_known_args()

    annoTokenClass = anno_token_types[args.corpus_type]

    if args.outfolder:
        if not os.path.exists(args.outfolder):
            os.makedirs(args.outfolder)
    else:
        args.outfolder = "."

    if not args.nosplit:
        outfiles = [
            (open(os.path.join(args.outfolder, args.corpus_name + '_train'), 'w'), args.trainsize),
            (open(os.path.join(args.outfolder, args.corpus_name + '_devel'), 'w'), args.develsize),
            (open(os.path.join(args.outfolder, args.corpus_name + '_test'), 'w'), args.testsize)
        ]
    else:
        outfiles = [
            (open(os.path.join(args.outfolder, args.corpus_name), 'w'), args.trainsize),
        ]

    for (_, _, files) in os.walk(args.corpus_folder):
        for filename in files:
            if filename.endswith('.xml'):
                print(filename)

                outfile_iter = iter(outfiles)

                token_count = 0
                current_file, current_size = next(outfile_iter)

                tree = ET.parse(args.corpus_folder + filename)
                root = tree.getroot()

                curr_sent = []
                sent_end = False
                for token_element in root.iter(annoTokenClass.get_element_name()):

                    token = annoTokenClass(token_element)
                    token_count += 1

                    if sent_end and not token.getBoundSent() == '$E':
                        current_file.write('\n'.join(['\t'.join(tok) for tok in curr_sent]))
                        current_file.write('\n\n')

                        ### check if enough tokens and switch file!
                        if not args.nosplit and token_count >= current_size:
                            try:
                                token_count = 0
                                current_file, current_size = next(outfile_iter)
                            except:
                                break

                        curr_sent = []

                    sent_end = False

                    curr_sent.append((token.getUTF(), token.getSimple(), token.getNorm(), token.getPOS(), token.getMSD(), token.getLemma()))

                    if token.getBoundSent().startswith('Satz') or token.getBoundSent() in ['DE', 'IE', 'EE', 'QE', '$E']:
                        sent_end = True

