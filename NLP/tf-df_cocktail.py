import nltk
import csv
import math
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import re
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
import pandas as pd
# nltk.download('punkt')
# nltk.download('stopwords') #載不下來在terminal 輸入python -m nltk.downloader stopwords
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
#------------------------------------------------------------------------------------------------------------------------
comment=[]
content=[]

with open(r'.\cocktail\finalV2.csv', newline='') as csvfile:

    # 以逗號分隔欄位，讀取檔案內容
    rows = csv.reader(csvfile, delimiter=',')
    # print(rows)
    for row in rows:
        e_comment = row[6]
        comment.append(e_comment)
        e_content = row[5]
        content.append(e_content)

comment_i = [i for i in comment if len(i) != 0][1:]#去除空值及標題
content_i = [i for i in content if len(i) != 0][1:]#去除空值及標題

remove_chars = '[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+' #移除數字及特殊符號
remove_1 = [re.sub(remove_chars, '', i) for i in comment_i ]
c = re.compile(' ')
document = [c.sub(' ', i)for i in remove_1] #移除空格


#------------------------------------------------------------------------------------------------------------------------
# #轉乘小寫、去除標點符號----------------------------------------------------------------------------------------------------
def get_tokens(text):
    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lowers.translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(no_punctuation)
    return tokens



##------------------------------------------------------------------------------------------------------------------------
# startswith(用于检查字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False
#詞性還原
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV #False
    else:
        return None

#--------------------資料清洗----------------------------------------------------------------------------------------------------
word_list =[] #全部文章的詞

for i in document :
    tokens = get_tokens(i) # 分词
    # print(tokens)
    #去除數字
    filtered = [w for w in tokens if not w in stopwords.words('english')] #過濾停用詞
    # print('filtered',filtered)
    tagged_sent = pos_tag(filtered)  # 获取单词词性..........('terrific', 'JJ'), ('cocktail', 'NN')..................?
    # print('tagged_sent',tagged_sent)
    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1])or wordnet.NOUN
        wnl_lemmatize = wnl.lemmatize(tag[0], pos=wordnet_pos)#词形还原
        lemmas_sent.append(wnl_lemmatize)  # 词形还原
    word_list.append(lemmas_sent)
print(word_list)
# ------------------------------------------------------------------------------------------------------------------------
#-------------計算詞頻
countlist = []
for i in range(len(word_list)):
    count = Counter(word_list[i])
    countlist.append(count)

#------------------------------------------------------------------------------------------------------------------------
# # 下面的程式碼實現了計算TF-IDF值的功能
# # 定義計算tfidf公式的函數
def tf(word, count):
    return count[word] / sum(count.values()) #count為'definitely': 1 字典形式
#
# # 統計的是含有該單詞的句子數
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)
#
# # len(count_list)是指句子的總數，n_containing(word, count_list)是指含有該單詞的句子的總數，
# # 加1是爲了防止分母爲0
def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing (word, count_list)))
#
# # 將tf和idf相乘
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)
#
#
# #------------------------------------------------------------------------------------------------------------------------
#enumerate 组合为一个索引序列 counlist是所有酒款的所有評論 #count 是每款酒的所有評論  #word是評論當中的關鍵字
for i, count in enumerate(countlist):
    print("Top words in document {}".format(i+1)) #看第幾個文件
    scores = {word: tfidf(word, count, countlist) for word in count}  #抓出在每款酒裡所有評論的word 組合成字典的形式，算出每個word的# tfidf值
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True) #sort是在原位重新排列列表，而sorted()是产生一个新的列表(list)。
    for word, score in sorted_words[:1]: #:從第一項取至幾項

        TF_IDF = ("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))#到小數點後五位
        print(TF_IDF)




# ------------------------------------------------------------------------------------------------------------------------
# 所有評論所出現的關鍵詞----------另一種方法算出tfidf
all_dict = {}
for c in countlist:
    counter = dict(c)
    for k, v in counter.items():
        try:
            all_dict[k] += v  #兩個以上的詞
        except:
            all_dict[k] = v  #只有出現一次的詞
print('merge-->', all_dict)
#
with open('tf.txt', 'w+') as tfin, open('idf.txt', 'w+')as idfin ,open('tfidf.txt','w+') as ifidfin :
    for k in all_dict.keys():

        k_tf = tf(k, all_dict)
        tfin.write(k + ' ' + str (k_tf) + '\n')
        # print(k_tf)
        k_idf = idf(k, countlist)
        idfin.write(k + ' ' + str(k_idf) + '\n')
        # print(k_idf)
        k_tfidf =tfidf(k,all_dict,countlist)
        # print('k_tfidf',k_tfidf)
        ifidfin.write(( k +' ' + str(k_tfidf) +'\n'))

#------------------------------------------------------------------------------------------------------------------------