import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from recommendations.models import Drug
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

# 可视化部分
# 设置matplotlib风格
sns.set(style="whitegrid")
# 设置字体，适配 Windows、macOS
try:
    rcParams['font.sans-serif'] = ['Arial Unicode MS'] # Mac 系统中文字体
except:
    rcParams['font.sans-serif'] = ['SimHei']  # Windows 系统中文字体
rcParams['axes.unicode_minus'] = False  # 确保负号正常显示

def generate_reason_count_plot():
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)

    # 统计每种疾病的药品数量
    reason_counts = data['reason'].value_counts()

    # 绘制柱状图
    plt.figure(figsize=(12, 6))
    reason_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('不同疾病对应药品数量', fontsize=16)
    plt.xlabel('疾病类型', fontsize=14)
    plt.ylabel('药品数量', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    return buffer

def generate_rating_histogram():
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)

    # 绘制直方图
    plt.figure(figsize=(10, 6))
    plt.hist(data['rating'], bins=10, edgecolor='black', alpha=0.7)
    plt.title('药品评分分布', fontsize=16)
    plt.xlabel('评分', fontsize=14)
    plt.ylabel('频率', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    return buffer

def generate_top_companies_plot():
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)

    # 按公司统计药品数量
    top_companies = data['name'].value_counts().head(10)

    # 绘制柱状图
    plt.figure(figsize=(12, 6))
    top_companies.plot(kind='bar', color='coral', edgecolor='black')
    plt.title('药品数量排名前10的公司', fontsize=16)
    plt.xlabel('公司名称', fontsize=14)
    plt.ylabel('药品数量', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    return buffer

# 推荐系统部分
# 数据处理和初始化
# 基于协同过滤的推荐
def initialize_data1():
    # 从数据库加载数据
    from .models import Drug
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)
    # 文本特征提取
    tfidf = TfidfVectorizer(stop_words='english')
    data['combined_text'] = data['name'] + ' ' + data['description'] + ' ' + data['reason']
    text_features = tfidf.fit_transform(data['combined_text'])
    # 数值特征归一化
    scaler = MinMaxScaler()
    rating_features = scaler.fit_transform(data[['rating']])
    # 合并文本和数值特征
    combined_features = hstack([text_features, rating_features])
    # 计算综合相似度
    cosine_sim = linear_kernel(combined_features, combined_features)
    # 创建索引映射
    indices = pd.Series(data.index, index=data['name']).drop_duplicates()
    return data, cosine_sim, indices

# 基于内容的推荐
def initialize_data2():
    # 从数据库加载数据
    from .models import Drug
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)
    # 文本特征提取
    tfidf = TfidfVectorizer(stop_words='english')
    data['combined_text'] = data['name'] + ' ' + data['description'] + ' ' + data['reason']
    text_features = tfidf.fit_transform(data['combined_text'])
    # 数值特征归一化
    scaler = MinMaxScaler()
    rating_features = scaler.fit_transform(data[['rating']])
    # 权重设定
    weight_text = 0.6  # 文本特征权重
    weight_rating = 0.4  # 数值特征权重
    # 分别计算文本特征和评分特征的相似度
    cosine_sim_text = linear_kernel(text_features, text_features)
    cosine_sim_rating = linear_kernel(rating_features, rating_features)
    # 融合相似度矩阵
    cosine_sim = weight_text * cosine_sim_text + weight_rating * cosine_sim_rating
    # 创建索引映射
    indices = pd.Series(data.index, index=data['name']).drop_duplicates()
    return data, cosine_sim, indices

# 基于标签的推荐
def initialize_data3():
    # 从数据库加载数据
    from .models import Drug
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)
    # 将标签字符串分割为列表
    data['Reason_List'] = data['reason'].apply(lambda x: x.split(', '))
    # 将标签转为多热编码矩阵
    mlb = MultiLabelBinarizer()
    tag_matrix = mlb.fit_transform(data['Reason_List'])
    # 计算标签的余弦相似度
    cosine_sim = cosine_similarity(tag_matrix)
    return data, cosine_sim

# 基于隐语义模型的推荐
def initialize_data4():
    # 从数据库加载数据
    from .models import Drug
    drugs = Drug.objects.all().values()
    data = pd.DataFrame(drugs)
    # 文本特征提取
    tfidf = TfidfVectorizer(stop_words='english')
    data['combined_text'] = data['name'] + ' ' + data['description'] + ' ' + data['reason']
    tfidf_matrix = tfidf.fit_transform(data['combined_text'])
    # 构建药品相似性矩阵
    drug_similarity = cosine_similarity(tfidf_matrix)
    # 使用 TruncatedSVD 降维
    n_components = 50  # 设定隐含特征的数量
    svd = TruncatedSVD(n_components=n_components)
    latent_matrix = svd.fit_transform(drug_similarity)
    return data, latent_matrix


# 推荐函数
# 基于协同过滤的推荐
def recommend_by_collaborative_filtering(drug_name, top_n=5):
    # 初始化数据
    data, cosine_sim, indices = initialize_data1()
    if drug_name not in indices:
        return f"药品 {drug_name} 不存在，请检查输入名称"
    # 获取药品索引
    idx = indices[drug_name]
    # 计算相似度并排序
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 获取前 top_n 个相似药品（排除自身）
    sim_scores = sim_scores[1:top_n + 1]
    drug_indices = [i[0] for i in sim_scores]
    # 返回推荐药品名称
    return data['name'].iloc[drug_indices]

# 基于内容的推荐
def recommend_by_contents(drug_name, top_n=5):
    # 初始化数据
    data, cosine_sim, indices = initialize_data2()
    if drug_name not in indices:
        return f"药品 {drug_name} 不存在，请检查输入名称"
    # 获取药品索引
    idx = indices[drug_name]
    # 计算相似度并排序
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 获取前 top_n 相似药品（排除自身）
    sim_scores = sim_scores[1:top_n + 1]
    drug_indices = [i[0] for i in sim_scores]
    # 返回推荐的药品名称
    return data['name'].iloc[drug_indices]

# 基于标签的推荐
def recommend_by_tags(drug_name, top_n=5):
    # 初始化数据
    data, cosine_sim = initialize_data3()
    if drug_name not in data['name'].values:
        return f"药品 {drug_name} 不存在，请检查输入名称"
    # 获取药品索引
    idx = data[data['name'] == drug_name].index[0]
    # 获取与该药品标签相似的药品
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 获取前 top_n 个相似药品（排除自身）
    sim_scores = sim_scores[1:top_n + 1]
    medicine_indices = [i[0] for i in sim_scores]
    # 返回推荐药品名称
    return data['name'].iloc[medicine_indices]

# 基于隐语义模型的推荐
def recommend_by_svd(drug_name, top_n=5):
    # 初始化数据
    data, latent_matrix = initialize_data4()
    if drug_name not in data['name'].values:
        return f"药品 {drug_name} 不存在，请检查输入名称"
    # 获取药品索引
    idx = data[data['name'] == drug_name].index[0]
    # 计算药品隐含特征的相似性分数
    scores = np.dot(latent_matrix, latent_matrix[idx])
    # 排序获取前 top_n 个药品
    sorted_indices = np.argsort(scores)[::-1][1:top_n + 1]  # 排除自身
    return data['name'].iloc[sorted_indices]