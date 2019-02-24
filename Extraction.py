import os
from stanfordcorenlp import StanfordCoreNLP
from graphviz import Source

# make sure nltk can find stanford-parser
# please check your stanford-parser version from brew output (in my case 3.6.0)
os.environ['CLASSPATH'] = r'/usr/local/Cellar/stanford-parser/3.6.0/libexec'

sentence = 'The brown fox is quick and he is jumping over the lazy dog'

sdp = StanfordCoreNLP()
result = list(sdp.raw_parse(sentence))

dep_tree_dot_repr = [parse for parse in result][0].to_dot()
source = Source(dep_tree_dot_repr, filename="dep_tree", format="png")
source.view()
