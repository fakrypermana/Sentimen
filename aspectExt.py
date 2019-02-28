from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=15000)  # , quiet=False, logging_level=logging.DEBUG)
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

def rmvSign(text):
    indexText = text.find('##') + 2

    return text[indexText:]

def sourceAspcets(text):
    indexText = text.find('##')

    return text[:indexText]

def asteriskRelation(depParse, source, target):
    for i, y in enumerate(depParse):
        #print('ini y[0] ',y[0],' |target', target,' |ini source ',source[1],' |ini y[1] ', y[1])
        if y[0] == target and source[1] == y[1]:
            return True

    return False

def resultInCsv(result, source, similarities):
    with open('./hasilakhir2.csv', 'w', newline='') as csvfile:
        fieldnames = ['source', 'result', 'similar']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(0, len(result)):
            writer.writerow({'source': source[x], 'result': result[x], 'similar': similarities[x]})

if __name__ == '__main__':
    sNLP = StanfordNLP()

    texts = loadDataset('./Data.csv')
    aspectFromSourceDatas = []
    resultAspects = []
    similarities = []
    total = 0
    presisi = 0
    recall = 0

    for x in range(0, len(texts)):
        aspect = ''
        aspectFromSourceData = ''
        isSuitable = 0
        onlyText = rmvSign(texts[x])
        parsed = sNLP.dependency_parse(onlyText)
        words = sNLP.lemma(onlyText)
        #print('hasil lemma',words)
        print('data ----------------------  ',x+1)

        for i, y in enumerate(parsed):
            #print('ini y[0] dst',y[0],y[1],y[2])
            if (y[0] == 'amod') and ((y[1] - y[2]) > 0): #adjectival modifier
                #aspect = words[y[1] - 1] + " adj mod"
                print('y1 bos ',y[1])
                aspect = words[y[1] - 1]

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'djob'): #direct object - changed from dobj to comp
                #aspect = words[y[2] - 1] + " dir obj"
                #print('y[0] ',y[0],' = target ',parsed)
                #print('y[1]', y[1],' = source ', 'djob')
                print('y1 bos ',y[1])
                aspect = words[y[2] - 1]

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'acomp'): #adjectival complement
                #aspect = words[y[2] - 1] + " adj com"
                print('y1 bos ',y[1])
                aspect = words[y[2] - 1]

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'cop'): #complement of a copular verb
                #aspect = words[y[2] - 1] + " com verb"
                print('y1 bos ',y[1])
                aspect = words[y[2] - 1]

            elif (y[0] == 'nsubjpass') and asteriskRelation(parsed, y, 'advmod'): #adverbial modifier to a passive verb
                #aspect = words[y[2] - 1] + " adv mod"
                print('y1 bos ',y[1])
                aspect = words[y[2] - 1]

            elif (y[0] == 'compound') and ((y[1] - y[2]) > 0): #compound noun
                #aspect = words[y[2] - 1] + " " + words[y[1] - 1]
                #aspect = words[y[1] - 1] + " com noun"
                print('y1 bos ',y[1])
                aspect = words[y[1] - 1]

        aspectFromSourceData = sourceAspcets(texts[x])
        print('source aspect ',aspectFromSourceData)
        isSuitable = 0 if aspectFromSourceData.find(aspect) < 0 else 1
        resultAspects.append(aspect)
        print('result aspect ',aspect)
        aspectFromSourceDatas.append(aspectFromSourceData)
        if isSuitable == 1:
            total = total + 1 #total isSuitable = 1
        print(isSuitable)
        similarities.append(isSuitable)
    print('data ',len(resultAspects))
    print('total hasil yang sesuai', total)
    print('recall ', total/len(resultAspects))
    resultInCsv(resultAspects, aspectFromSourceDatas, similarities)
