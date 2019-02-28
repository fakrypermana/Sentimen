from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9001):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        # self.props = {
        #     'annotators': 'tokenize, pos, lemma',
        #     'pipelineLanguage': 'en',
        #     'outputFormat': 'json'
        # }

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def lemma(self, sentence):
        r_dict = self.nlp._request('ssplit,tokenize,lemma', sentence)
        tokens = [token['lemma'] for s in r_dict['sentences'] for token in s['tokens']]

        return tokens

def loadDataset(fileData):
    data = []

    with open(fileData) as csvfile:
        lines = csv.reader(csvfile)

        dataset = list(lines)

        for x in range(0, len(dataset)):
            data.append(dataset[x][0])

    return data

def purify(text):
    indexText = text.find('##') + 2

    return text[indexText:]

def sourceAspcets(text):
    indexText = text.find('##')

    return text[:indexText]

def hasRelation(depParse, source, target):
    for i, y in enumerate(depParse):
        #print('ini y[0] ',y[0],'target', target)
        if y[0] == target and source[1] == y[1]:
            return True

    return False

def saveToCsv(result, source, similarities):
    with open('./hasilakhir2.csv', 'w', newline='') as csvfile:
        fieldnames = ['source', 'result', 'similar']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(0, 300):
            writer.writerow({'source': source[x], 'result': result[x], 'similar': similarities[x]})

if __name__ == '__main__':
    sNLP = StanfordNLP()

    # print ("POS:", sNLP.pos(text))
    texts = loadDataset('./Data.csv')
    sourceAspects = []
    resultAspects = []
    similarities = []
    total = 0

    for x in range(0, 300):
        aspect = ''
        sourceAspect = ''
        similarity = 0
        cleanText = purify(texts[x])
        resultDep = sNLP.dependency_parse(cleanText)
        words = sNLP.lemma(cleanText)
        print('hasil lemma',words)

        for i, y in enumerate(resultDep):
            #print('ini y[0] dst',y[0],y[1],y[2])
            if (y[0] == 'amod') and ((y[1] - y[2]) > 0): #adjectival modifier
                #aspect = words[y[1] - 1] + " adj mod"
                aspect = words[y[1] - 1]

            elif (y[0] == 'nsubj') and hasRelation(resultDep, y, 'xcomp'): #direct object - changed from dobj to comp
                #aspect = words[y[2] - 1] + " dir obj"
                aspect = words[y[2] - 1]
                
            elif (y[0] == 'nsubj') and hasRelation(resultDep, y, 'acomp'): #adjectival complement
                #aspect = words[y[2] - 1] + " adj com"
                aspect = words[y[2] - 1]

            elif (y[0] == 'nsubj') and hasRelation(resultDep, y, 'cop'): #complement of a copular verb
                #aspect = words[y[2] - 1] + " com verb"
                aspect = words[y[2] - 1]

            elif (y[0] == 'nsubjpass') and hasRelation(resultDep, y, 'advmod'): #adverbial modifier to a passive verb
                #aspect = words[y[2] - 1] + " adv mod"
                aspect = words[y[2] - 1]

            elif (y[0] == 'compound') and ((y[1] - y[2]) > 0): #compound noun
                #aspect = words[y[2] - 1] + " " + words[y[1] - 1]
                #aspect = words[y[1] - 1] + " com noun"
                aspect = words[y[1] - 1]

        sourceAspect = sourceAspcets(texts[x])
        similarity = 0 if sourceAspect.find(aspect) < 0 else 1
        resultAspects.append(aspect)
        sourceAspects.append(sourceAspect)
        if similarity == 1:
            total = total + 1
        print('similatity ',total)
        similarities.append(similarity)

    saveToCsv(resultAspects, sourceAspects, similarities)
