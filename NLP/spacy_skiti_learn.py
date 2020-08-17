import pandas as pd
import csv
import re
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
#spacy------------------------------
import spacy
# print('spaCy Version: %s' % (spacy.__version__))  # spaCy Version: 2.3.2
import en_core_web_sm
import en_core_web_lg
from spacy.lang.en import English
from spacy.tokens import Doc
from spacy.symbols import PUNCT, NUM, AUX, X, CONJ, ADJ, VERB, PART, SPACE, CCONJ,INTJ,NOUN
from spacy.lang.en.stop_words import STOP_WORDS
#---------------------------------------
nlp = spacy.load('en_core_web_lg')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
spacy_stopwords = spacy_stopwords.union({
    'easy', 'long', 'nice', 'tasty',
    'great', 'good','username','text','oz','sure'})
# print('Number of stop words: %d' % len(spacy_stopwords))
# print('First ten stop words: %s' % list(spacy_stopwords)[:])
#---------------------------------------
df = pd.read_csv(r'.\cocktail\cocktail_all_combine.csv',encoding='utf-8-sig')

df['mix'] = '['+ df['ins'].map(str)+']' +df['comment'].map(str)+'\r'+'\r'+df['favor'].map(str)+'\r''\r'+ df['Vodka'].map(str)+'\r'+ df['Rum'].map(str)+'\r'+ df['Gin'].map(str)+'\r'+ df['Tequila'].map(str)+'\r'+'\r'+''+ df['Whiskey'].map(str)+'\r'+'\r'+ df['Brandy'].map(str)+'\r'+ df['liqueur'].map(str)+']'

dff = df[df['mix'] != '[nan]nannannannannannannannan']
data = list(dff['mix'])
data_i = [i.lower().replace('nan','').strip().strip('\r').strip('\\').strip('\t') for i in data if len(i) != 0]

remove_chars = '[0-9’!"#$%&()*+-./:;<=>?@，。?★、…【】\'\r《》？“”‘’！\\\\[\\]^_`{|}~]+' #移除數字及特殊符號
remove = [re.sub(remove_chars, '' , i) for i in data_i]
# text = [re.compile('').sub('', i)for i in remove if len(i) != 0] #移除空格
text = [re.compile('').sub('', i)for i in remove]

# print(index)
name = list(dff['name'])
##-----------------------------查看資訊-------------------------
'''
# for token in nlp(str(text[0:10])):
#     # if  token.pos_ == 'ADJ' or  token.pos_ == 'NOUN':
#     #     print('token.text:',token.text,'token.lemma_:',token.lemma_,'token.pos_:',token.pos_,'token.tag_:',token.tag_)
#
#     print('token.text:',token.text,'token.lemma_:',token.lemma_,'token.pos_:',token.pos_,'token.tag_:',token.tag_,
#     'token.dep_:',token.dep_,'token.shape_:', token.shape_,'token.is_alpha:',token.is_alpha,'token.is_stop:',token.is_stop)
'''
# # #-----------------------用正則及CountVectorizer做詞性還原及分詞-及停用詞-------------------------------------------------
# lemma_data = []
# for idx, item in enumerate(text):
#     doc = nlp(item)  # --> set the document vocab
#     doc_spacy = Doc(doc.vocab, words=[t.text for t in doc]) #vocab：詞彙表
#     token_lemma_data = [token.lemma_ for token in doc_spacy if not token.is_stop]
#
#     # print(token_lemma_data)
#     lemma_data.append(token_lemma_data)
# corpus = [str(item).strip().replace('\\','').replace('\t','') for item in lemma_data if len(str(item)) > 1]
# print('corpus',corpus)
# # # -----------------詞性還原 及 詞性標註(只留形容詞、感嘆詞、名詞)---------------------------------------
# # #
pos_data =[]
for n, item in enumerate(text):
    doc = nlp(item)
    # pos = [token.pos_ for token in doc]
    # doc_spacy = Doc(doc.vocab, words=[t.text for t in doc])
    no_VERB = [token.lemma_ for token in doc if token.pos_ == 'ADJ' ] #or token.pos_ == 'NOUN'or token.pos_ == 'PROPN'
    pos_data.append(no_VERB)
# print('pos_data',pos_data)
pos = [str(item).strip().replace('\\','').replace('\t','') for item in pos_data if len(str(item)) > 1]
print('pos',pos)

# # # ---------------------------------------------------------------
# # # # # 計算單字次數：
vect = CountVectorizer(token_pattern='(?u)\\b\\w\\w+\\b',stop_words=spacy_stopwords,min_df=0.005)#,max_df=0.99,min_df=0.01)
x_train = vect.fit_transform(pos)
feature = vect.get_feature_names()
print(feature)
# # # # # #------------dataframe貯存---------------------
count_feature = pd.DataFrame(x_train.toarray(), columns=feature, index=name)
print('dataframe:',count_feature)
count_feature.to_csv(r'./cocktail/tfidf/mix_pos_feature_matrix_0809.csv', encoding='utf-8-sig')
# # # # # ---------------------------------------------------------------
# # # #計算tfidf權重--------------------------------------
transformer = TfidfTransformer()
tfidf_matrix = transformer.fit_transform(x_train)
weight = tfidf_matrix.toarray()
# # # #------------dataframe貯存---------------------
tfidf = pd.DataFrame(tfidf_matrix.toarray(),columns=feature,index=name)
print('tfidf_matrix:',tfidf)
tfidf.to_csv(r'./cocktail/tfidf/tfidf_min0.005_pos_matrix_0809.csv', encoding='utf-8-sig')


# 数据标准化-------------------------------------------------
from sklearn import preprocessing

'''
preprocessing.scale()是按照列进行标准化计算，计算公式为:
(X_train[:,0]-X_train[:,0].mean())/X_train[:,0].std()
(X_train[:,0]-np.mean(X_train[:,0]))/np.std(X_train[:,0])//或者
'''
X_scaled = preprocessing.scale(weight)  # scale操作之后的数据零均值，单位方差（方差为1）
print(X_scaled)
print('#-----------------------------------')
# # # # # #-------------------------------------------------------------------------------------------------------
# # 进行PCA数据降维
from sklearn.decomposition import PCA
#
# # 生成PCA实例
pca = PCA(n_components=3)  # 把维度降至3维
# # 进行PCA降维
X_pca = pca.fit_transform(X_scaled)
print(X_pca)
# # 生成降维后的dataframe
X_pca_frame = pd.DataFrame(X_pca, columns=['pca_1', 'pca_2', 'pca_3'])  # 原始数据由(30000, 7)降维至(30000, 3)
print(X_pca_frame)
# # # # # #--------------------kmeans--------------------------------------------
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
# # #
from sklearn.manifold import TSNE
# # 指定分成5个类
clf = KMeans(n_clusters=7)
kmean = clf.fit(X_pca)#開始訓練！
print(kmean.cluster_centers_)
# # 打印出各个族的中心点
for index ,label in enumerate(kmean.labels_,1):
    print('index:{},label:{}'.format(index,label))
# # 样本距其最近的聚类中心的平方距离之和，用来评判分类的准确度，值越小越好
# # k-means的超参数n_clusters可以通过该值来评估
print("inertia: {}".format(kmean.inertia_))
# # #
# #
# # # 使用T-SNE算法，对权重进行降维，准确度比PCA算法高，但是耗时长
tsne = TSNE(n_components=3,init='pca', random_state=501) #嵌入空间的维度
decomposition_data = tsne.fit_transform(weight)
print("Org data dimension is {}.Embedded data dimension is {}".format(weight.shape[-1], decomposition_data.shape[-1]))
#
x = []
y = []
# #
for i in decomposition_data:
    x.append(i[0])
    y.append(i[1])
#
print(x)
print(y)
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()
plt.scatter(x, y, c=kmean.labels_, marker="x")
plt.xticks(())
plt.yticks(())
plt.show()
plt.savefig('./sample.png')
# --------------------LDA 狄利克雷分布 找出潛在主題-------------------------------------
from sklearn.decomposition import LatentDirichletAllocation
vect_lda= CountVectorizer(stop_words=spacy_stopwords,max_df=0.15)
x = vect_lda.fit_transform(pos)
# print(x)
n_components = 7
lda = LatentDirichletAllocation(n_components=n_components,learning_method="batch",max_iter=50,random_state=0)
document_topics = lda.fit_transform(x)
shape = lda.components_.shape

def print_top_words(model, feature_names, n_top_words):
    #打印每个主题下权重较高的term
    for topic_idx, topic in enumerate(model.components_):
        print( "Topic #%d:" % topic_idx)
        print( " ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
    #打印主题-词语分布矩阵
    print(model.components_)

n_top_words=10
tf_feature_names = vect_lda.get_feature_names()
print(tf_feature_names )
top_word = print_top_words(lda, tf_feature_names, n_top_words)
print(top_word)