from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=15000)  # , quiet=False, logging_level=logging.DEBUG)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def lemma(self, sentence):
        r_dict = self.nlp._request('ssplit,tokenize,lemma', sentence)
        tokens = [token['lemma'] for s in r_dict['sentences'] for token in s['tokens']]

        return tokens

def loadData(fileData):
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

def sourceAspek(text):
    indexText = text.find('##')

    return text[:indexText]

def asteriskRelation(depParse, source, target):
    for i, y in enumerate(depParse):
        #print('ini y[0] ',y[0],' |target', target,' |ini source ',source[1],' |ini y[1] ', y[1])
        if y[0] == target and source[1] == y[1]:
            return True

    return False

def countPrecRecall(aspect,source):
    total = 0
    i = 0

    for x in aspect:
        for y in source:
            isSuitable = 0 if x.find(y) < 0 else 1
            if isSuitable == 1:
                total = total + 1 #total isSuitable = 1
                #print('nambah pas di date ke ',y)
    return total

def resultInCsv(result, source, similarities):
    with open('./hasil.csv', '`w', newline='') as csvfile:
        fieldnames = ['source', 'result', 'similar']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for x in range(0, len(result)):
            writer.writerow({'source': source[x], 'result': result[x], 'similar': similarities[x]})

if __name__ == '__main__':
    sNLP = StanfordNLP()

    texts = loadData('./Data.csv')
    aspectFromSourceDatas = []
    resultAspects = []
    similarities = []
    total = 0

    for x in range(0, len(texts)):
        #aspect = ''
        aspect = []
        aspectFromSourceData = ''
        type = ''
        isSuitable = 0
        onlyText = rmvSign(texts[x])
        parsed = sNLP.dependency_parse(onlyText)
        words = sNLP.lemma(onlyText)
        #print('hasil lemma',words)
        print('data ----------------------  ',x+1)

        for i, y in enumerate(parsed):
            #print('ini y[0] dst',y[0],y[1],y[2])
            if (y[0] == 'amod') and ((y[1] - y[2]) > 0): #adjectival modifier
                #aspect = words[y[1] - 1]
                aspect.append(words[y[1] - 1])
                print('kata ke ',y[1] - 1)
                print('words ', words[y[1] - 1])
                print('type : adj mod')
                # aspect = words[y[1] - 1]

            #elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'xcomp'): #direct object - changed from dobj to comp
            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'djob'):
                #aspect = words[y[2] - 1]
                aspect.append(words[y[2] - 1])
                #print('y[0] ',y[0],' = target ',parsed)
                #print('y[1]', y[1],' = source ', 'djob')
                print('kata ke ',y[2]- 1)
                print('words ', words[y[2] - 1])
                print('type : dir obj')
                # aspect = words[y[2] - 1]

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'acomp'): #adjectival complement
                #aspect = words[y[2] - 1]
                aspect.append(words[y[2] - 1])
                print('kata ke ',y[2]- 1)
                print('words ', words[y[2] - 1])
                print('type : adj com')
                # aspect = words[y[2] - 1]

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'cop'): #complement of a copular verb
                #aspect = words[y[2] - 1]
                aspect.append(words[y[2] - 1])
                print('kata ke ',y[2]- 1)
                print('words ', words[y[2] - 1])
                print('type : com verb')
                # aspect = words[y[2] - 1]

            elif (y[0] == 'nsubjpass') and asteriskRelation(parsed, y, 'advmod'): #adverbial modifier to a passive verb
                #aspect = words[y[2] - 1]
                aspect.append(words[y[2] - 1])
                print('kata ke ',y[2]- 1)
                print('words ', words[y[2] - 1])
                print('type : adv mob')
                # aspect = words[y[2] - 1]

            elif (y[0] == 'compound') and ((y[1] - y[2]) > 0): #compound noun
                #aspect = words[y[2] - 1] + " " + words[y[1] - 1]
                #aspect = words[y[1] - 1]
                aspect.append(words[y[1] - 1])
                print('kata ke ',y[1]- 1)
                print('words ', words[y[1] - 1])
                print('type : com noun')
                # aspect = words[y[1] - 1]

        aspectFromSourceData = sourceAspek(texts[x])
        print('source aspect ',aspectFromSourceData)
        #isSuitable = 0 if aspectFromSourceData.find(aspect) < 0 else 1
        resultAspects.append(aspect)
        print('result aspect ',aspect)
        aspectFromSourceDatas.append(aspectFromSourceData)
        total = countPrecRecall(aspect,aspectFromSourceData)
        # if isSuitable == 1:
        #     total = total + 1 #total isSuitable = 1
        # print('is suitable ? ',isSuitable)
        # similarities.append(isSuitable)
    print('===================================')
    print('data ',len(resultAspects))
    print('total hasil yang sesuai', total)
    #print('recall ', total/len(resultAspects))
    #resultInCsv(resultAspects, aspectFromSourceDatas, similarities)
