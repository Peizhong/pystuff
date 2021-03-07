from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# built-in machine learning algorithms and models, called estimators
clf = RandomForestClassifier(random_state=0)
X = [[ 1,  2,  3],  # 2 samples, 3 features
     [11, 12, 13]]
y = [0, 1]  # classes of each sample
# x: samples matrix, size of X is typically (n_samples, n_features) 
# y: real numbers for regression tasks
clf.fit(X, y)

clf.predict(X)

testPd = clf.predict([[4, 5, 6], [14, 15, 16]])
print(testPd)

# Machine learning workflows are often composed of different parts, pipeline
## StandardScaler mean平均数/standard deviation标准差
transX = StandardScaler().fit(X).transform(X)
print(transX)

# create a pipeline object
pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression()
)
# load the iris dataset and split it into train and test sets
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# fit the whole pipeline
pipe.fit(X_train, y_train)
score = accuracy_score(pipe.predict(X_test), y_test)
print(score)

# SVM Support vector machines, 支持向量机
# 寻找最优分界线，到两边的margin都最大。平面/超平面，离两边一样远。如果低维空间找不到合适的超平面，那就升维到更高维度去寻找超平面
# kernel函数：在低维空间里面去评估n维空间下超平面的效果，减少维度计算，提高分类效率
# 对问题真实模型的逼近，允许某些点不正确，但会增加惩罚

# 异常检测(Outlier Detection)

# 分类和回归

# 机器学习，神经网络

# 数据集：训练 验证 测试

# 分类，回归

