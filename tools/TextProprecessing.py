# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 19:09:14 2016

@author: z00383161
"""

import jieba
import jieba.analyse
import re
import codecs
import string
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import numpy
import pandas

class TextCleanTools(object):
    
    http_reg = re.compile(r'[a-zA-z]+://[^\s\u4e00-\u9fd5]*')
    email_reg = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')

    re_sentence_splitter = re.compile(r'[。！？!?]')
    #return reobj.split(input_str)

    # punctuation regex pattern
    # english punctuations: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    english_punctuations = string.punctuation
    chinese_punctuations = '''！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝
        ～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.'''.decode("utf-8")
    punctuations_pattern = re.compile(ur"^[%s%s]+" % (chinese_punctuations, english_punctuations))
    
    # digital regex pattern
    # integer, real, percent%
    digital_pattern =  re.compile(r"-?\d+[.%]?\d+[%]?")
    
    # english word regex pattern
    english_word_pattern = re.compile(r"\w+")
    
    # stop words list
    english_stopwords = [line.strip() for line in codecs.open('english_stopwords.txt',encoding='utf-8')]
    chinese_stopwords = [line.strip() for line in codecs.open('chinese_stopwords.txt',encoding='utf-8')]
     
    porter = PorterStemmer()
    wnl = WordNetLemmatizer()
    
    def __init__(self):
        pass
    
    def is_punctuations(self, word):
        return self.punctuations_pattern.search(word)
        
    def is_number(self, word):
        return self.digital_pattern.search(word)
    
    def is_englishword(self, word):
        return self.english_word_pattern.search(word)
    
    def clean_words(self, wordlist):
        cleaned_list = []
        for word in wordlist:
            if self.is_punctuations(word):
                continue
            
            if self.is_number(word):
                continue
            
            if self.is_englishword(word):
                if (len(word) > 2) and (not word in self.english_stopwords):
                    cleaned_word = word.lower()
                    cleaned_word = self.porter.stem(cleaned_word)
                    cleaned_word = self.wnl.lemmatize(cleaned_word)
                    cleaned_list.append(cleaned_word)
            else:
                if (len(word) > 1) and (not word in self.chinese_stopwords):
                    cleaned_list.append(word)
        
        return cleaned_list

                
if __name__ == '__main__':

    txtfile = codecs.open("news_test.txt", 'r', 'utf-8')
    words = []
    txt_clean_tools = TextCleanTools()
    
    # textrank(self, sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'), withFlag=False)
    
    for line in txtfile.readlines():
        segs = jieba.cut(line)
        nonempty_words = [s.strip() for s in segs if len(s.strip()) > 0]
        words = words + txt_clean_tools.clean_words(nonempty_words)
        
        keywords = jieba.analyse.textrank(line, topK=8)
        print "-".join(keywords)
        
    #print "---".join(words)
    #print len(set(words))
    
    wordDF = pandas.DataFrame({'words': words})
    wordStat = wordDF.groupby(by=["words"])["words"] \
        .agg({"wordcount":numpy.size}) \
        .reset_index() \
        .sort_values(by=["wordcount"], ascending=False);
    print wordStat.head(50)
    #print wordStat.shape[0]
    
    txtfile.close()
    
