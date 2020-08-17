#------------------PCA降維-------------------------------------------------
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from joblib import dump, load
from mpl_toolkits.mplot3d import Axes3D  # 绘制3D图形
from sklearn import metrics
import matplotlib.pyplot as plt

X = pd.read_csv(r'./cocktail/tfidf/tfidf_min0.005_pos_matrix_0809.csv', encoding='utf-8') #0802做過
X = X.drop(['Unnamed: 0'], axis=1)
#-----------------------------------
X_scaled = preprocessing.scale(X)  # scale操作之后的数据零均值，单位方差（方差为1）
#-----------------------------------
pca = PCA(n_components=3)  # 把维度降至3维
X_pca = pca.fit_transform(X_scaled)
# # 生成降维后的dataframe
X_pca_frame = pd.DataFrame(X_pca, columns=['pca_1', 'pca_2', 'pca_3'])  # 原始数据由(30000, 7)降维至(30000, 3)
est = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
       n_clusters=11, n_init=10, random_state=0, tol=0.0001, verbose=0)
est.fit(X_pca)
dump(est, r'./cocktail/model/kmeans-cocktail.joblib')

# # 取出聚类后的标签
kmeans_clustering_labels = pd.DataFrame(est.labels_, columns=['cluster'])  # 0-9,一共10个标签
X_pca_frame = pd.concat([X_pca_frame, kmeans_clustering_labels], axis=1)


X.index = X_pca_frame.index  # 返回：RangeIndex(start=0, stop=30000, step=1)
# 合并原数据和三个主成分的数据
X_full = pd.concat([X, X_pca_frame], axis=1)
# X_full.to_csv(r'./cocktail/tfidf/kmeans_matrix_0811.csv',encoding='utf-8')
# print(X_full)

clf = load(r'./cocktail/model/kmeans-cocktail.joblib')

#-----------------------------------

# 生成三维图形，每个样本点的坐标分别是三个主成分的值
# 设置每个簇对应的颜色
cluster_2_color = {0: 'peru', 1: 'burlywood', 2: 'steelblue', 3: 'gold', 4: 'turquoise', 5: 'lightslategray', 6: 'silver', 7: 'lightcoral',
                   8: 'yellowgreen', 9: 'olive',10: 'brown'}#,11: 'darkcyan',12: 'darkgoldenrod'}

# 按每个聚类分组
grouped = X_full.groupby('cluster')
result_data = pd.DataFrame()
for name, group in grouped:
    # print(group)
    desp = group[['pca_1', 'pca_2', 'pca_3']].describe()  # 返回每组的数量、均值、标准差、最小值、最大值等数据
    # print(desp)
# # #  # 每组未去除异常值的个数
    print('Group:{0}, Samples before:{1}'.format(name, group['pca_1'].count()))
#
    for att in ['pca_1', 'pca_2', 'pca_3']:
        # 去异常值：箱形图

        lower25 = desp.loc['25%', att] #Q1
        upper75 = desp.loc['75%', att] #Q3
        IQR = upper75 - lower25
        # print(IQR)
        min_value = lower25 - 1.5 * IQR
        max_value = upper75 + 1.5 * IQR
#         # 使用统计中的1.5*IQR法则，删除每个聚类中的噪音和异常点
        group = group[(group[att] > min_value) & (group[att] < max_value)]
    result_data = pd.concat([result_data, group], axis=0)
    # print(result_data)
# #      # 每组去除异常值后的个数
    print('Group:{0}, Samples after:{1}'.format(name, group['pca_1'].count()))
print('Remain sample:', result_data['pca_1'].count())
# # # # #--------------------------------------------------------
# # # 筛选后的数据聚类可视化
#
colors_filtered_data = result_data.cluster.map(cluster_2_color)
fig = plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(result_data.pca_1.values, result_data.pca_2.values, result_data.pca_3.values, c=colors_filtered_data)
ax.set_xlabel('Component_1')
ax.set_ylabel('Component_2')
ax.set_zlabel('Component_3')
plt.show()