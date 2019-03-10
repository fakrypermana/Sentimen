from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import math

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

def stringSource(text):
    indextText = text.find('[')

    return text[:indextText]

def asteriskRelation(depParse, source, target):
    for i, y in enumerate(depParse):
        if y[0] == target and source[1] == y[1]:
            return True

    return False

def checkSameAspect(aspect):
    realAspect = ''

    for x in aspect:
        for y in aspect:
            if x == y :
                realAspect = x

    return realAspect

def countExtractedAspect(aspect,source,total,i):

    for x in aspect:
        isSuitable = 0 if x.find(source) < 0 else 1
        if (len(x) != 0 and len(source) == 0) or (len(x) == 0 and len(source) != 0):
            isSuitable = -1
        if isSuitable == 1:
            total = total + 1 #total isSuitable = 1

        i = i +1
    return total,i

def totalAspectFromSource(aspect, totalAspectSource):
    print('ampun mak',aspect.split(','))
    listAspect = []
    words = aspect.split(',')
    for i in words :
        listAspect.append(i)

    totalAspectSource = totalAspectSource + len(listAspect)

    return totalAspectSource

# def resultInCsv(result, source, similarities):
#     with open('./hasil.csv', '`w', newline='') as csvfile:
#         fieldnames = ['source', 'result', 'similar']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#
#         for x in range(0, len(result)):
#             writer.writerow({'source': source[x], 'result': result[x], 'similar': similarities[x]})

if __name__ == '__main__':
    sNLP = StanfordNLP()

    texts = loadData('./Data.csv')
    aspectFromSourceDatas = []
    resultAspects = []
    similarities = []
    total = 0
    totalAspectSource = 0
    aspectTryed = 0
    grafikPrecision = []
    grafikRecall = []
    sumbuVertical = 0
    sumbuX = []

    for x in range(0, len(texts)):
        aspect = []
        realAspect = []
        aspectFromSourceData = ''
        type = ''
        isSuitable = 0
        onlyText = rmvSign(texts[x])
        parsed = sNLP.dependency_parse(onlyText)
        words = sNLP.lemma(onlyText)
        print('data ----------------------  ',x+1)
        sumbuVertical = sumbuVertical + 1
        sumbuX.append(sumbuVertical)


        for i, y in enumerate(parsed):
            if (y[0] == 'amod') and ((y[1] - y[2]) > 0): #adjectival modifier
                #aspect = words[y[1] - 1]
                aspect.append(words[y[1] - 1])
                print('kata ke ',y[1] - 1)
                print('words ', words[y[1] - 1])
                print('type : adj mod')

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'djob'):
                aspect.append(words[y[2] - 1])
                print('kata ke ',y[2]- 1)
                print('words ', words[y[2] - 1])
                print('type : dir obj')

            elif (y[0] == 'nsubj') and asteriskRelation(parsed, y, 'acomp'): #adjectival complement
                aspect.append(words[y[2] - 1])
                print('kata ke ',y[2]- 1)
                print('words ', words[y[2] - 1])
                print('type : adj com')

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
                aspect.append(words[y[1] - 1])
                print('kata ke ',y[1]- 1)
                print('words ', words[y[1] - 1])
                print('type : com noun')

        aspectFromSourceData = sourceAspek(texts[x])
        totalAspectSource = totalAspectFromSource(aspectFromSourceData,totalAspectSource)
        print('length source aspect',totalAspectSource)
        aspectWithoutValue = stringSource(aspectFromSourceData)
        print('source aspect ',aspectFromSourceData)
        resultAspects.append(aspect)
        print('result aspect ',aspect)
        aspectFromSourceDatas.append(aspectWithoutValue)
        total,aspectTryed = countExtractedAspect(aspect,aspectWithoutValue,total,aspectTryed)
        precision = (total / aspectTryed *100)
        recall = (total / totalAspectSource *100)
        grafikPrecision.append(precision)
        grafikRecall.append(recall)

        # print('ini precision ',precision)
        # print('ini recall ',recall)
        # print('aspektryed',aspectTryed)
        # print('ini total ',total)

    print('===================================')
    print('               OUTPUT              ')
    print('===================================')
    totalPrecision = total / aspectTryed
    totalRecall = total / totalAspectSource
    print('data      :',len(resultAspects))
    print('precision :',totalPrecision*100,'%')
    print('recall    :',totalRecall*100,'%')

    #Grafik
    plt.plot(sumbuX,grafikPrecision, label="Precision")
    plt.plot(sumbuX,grafikRecall, label="Recall")
    plt.legend(loc='upper left')
    plt.xlabel('data ke ')
    plt.ylabel('besar precision & recall dalam %')
    plt.show()

