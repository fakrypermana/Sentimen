from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import csv
import re

class StanfordNLP:
    def __init__(self, host='http://localhost', port=9001):
        self.nlp = StanfordCoreNLP(host, port=port,
                                   timeout=30000)
        self.props = {
            'annotators': 'depparse',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

def loadDataset(fileData):
    data = []


    with open(fileData) as csvfile:
        readCSV = csv.reader(csvfile)
        dataset = []
        for row in readCSV:
            # print(row)
            x = re.sub(r'.*##', '', str(row))
            x = x[:-2]
            dataset.append(x)

    return dataset
            # print(x)
            # text = nltk.word_tokenize(str(x))
            # print(nltk.pos_tag(text))

    # with open(fileData) as csvfile:
    #     lines = csv.reader(csvfile)
    #
    #     dataset = list(lines)
    #
    #     for x in range(0, 300):
    #         data.append(dataset[x][0])
    #
    # return data

if __name__ == '__main__':
    sNLP = StanfordNLP()

    texts = loadDataset('Data.csv')
    text = "The movie had an excellent storyline!"

    for x in range(0, 300):
        print("Dep Parser - ",x,":", sNLP.dependency_parse(texts[x]))
        # y = sNLP.dependency_parse(text[x])
        # for i in y :
        #     if i[0] == "amod":
        #         print('aspek :',i[1])
