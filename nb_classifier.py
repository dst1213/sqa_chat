from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle


class NBClassifier:

    def __init__(self, pos_file, neg_file, model_file,vectorizer_file):
        self.pos_file = pos_file
        self.neg_file = neg_file
        self.model_file = model_file
        self.vectorizer_file = vectorizer_file
        self.positive_samples = self.negative_samples = []
        self.load_data()

    def load_data(self):
        with open(self.pos_file, "r", encoding="utf8") as pf:
            self.positive_samples = pf.readlines()

        with open(self.neg_file, "r", encoding="utf8") as nf:
            self.negative_samples = nf.readlines()

    def save_model_pickle(self):
        with open(self.model_file, 'wb') as file:
            pickle.dump(self.clf, file)
        with open(self.vectorizer_file, 'wb') as file:
            pickle.dump(self.vectorizer, file)
    def load_model_pickle(self):
        with open(self.model_file, 'rb') as file:
            model =  pickle.load(file)
        with open(self.vectorizer_file, 'rb') as file:
            vectorizer =  pickle.load(file)
        return model,vectorizer
    def train(self):
        # 建立词袋模型
        self.vectorizer = CountVectorizer()

        # 将所有样本放入一个列表中
        all_samples = self.positive_samples + self.negative_samples
        labels = [1] * len(self.positive_samples) + [0] * len(self.negative_samples)  # 1代表正例，0代表负例

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(all_samples, labels, test_size=0.2)  # , random_state=42)

        # 在训练集上训练词袋模型，并转化文本数据
        X_train_vec = self.vectorizer.fit_transform(X_train)

        # 使用朴素贝叶斯分类器训练模型
        self.clf = MultinomialNB()
        self.clf.fit(X_train_vec, y_train)

        # 保存模型
        self.save_model_pickle()

        # 在测试集上评估模型
        X_test_vec = self.vectorizer.transform(X_test)
        y_pred = self.clf.predict(X_test_vec)

        print(classification_report(y_test, y_pred, zero_division=1))


class NBPredictor:

    def __init__(self, model_file,vectorizer_file):
        self.model_file = model_file
        self.vectorizer_file = vectorizer_file
        self.model, self.vectorizer = self.load_model_pickle()

    def load_model_pickle(self):
        with open(self.model_file, 'rb') as file:
            model = pickle.load(file)
        with open(self.vectorizer_file, 'rb') as file:
            vectorizer = pickle.load(file)
        return model, vectorizer
    def predict_spam(self, text):
        text_vectorized = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorized)
        return True if prediction[0] == 1 else False


if __name__ == "__main__":
    # 数据
    pos_file = r"data/nb_pos.txt"
    neg_file = r"data/nb_neg.txt"
    model_file = r"data/nb_clf.pkl"
    vectorizer_file = r"data/nb_vec.pkl"
    # 训练
    # nb_model = NBClassifier(pos_file, neg_file, model_file,vectorizer_file)
    # nb_model.train()

    # 预测
    nb_predict = NBPredictor(model_file,vectorizer_file)


    text = "Today's research for tomorrow's cure"
    prediction = nb_predict.predict_spam(text)
    print(prediction)

    text = '"work_experience": "Search Stanford,SU Home,Copyright Complaints,Maps & Directions,Terms of Use"'
    prediction = nb_predict.predict_spam(text)
    print(prediction)

    text = '"academic": "Professor,  Epidemiology and Population Health,Member,  Stanford Cancer Institute,Professor (By courtesy),  Biomedical Data Science,Professor (By courtesy),  Statistics,Professor,  Medicine - Stanford Prevention Research Center,Member,  Bio-X,Member,  Cardiovascular Institute,Affiliate,  Stanford Woods Institute for the Environment"'
    prediction = nb_predict.predict_spam(text)
    print(prediction)

    text = 'SU Home,Copyright Complaints,Maps & Directions,Search Stanford,Terms of Use'
    prediction = nb_predict.predict_spam(text)
    print(prediction)