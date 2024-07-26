from flask import Flask, request, jsonify
from matplotlib import pyplot as plt
import pandas as pd
import re
import pickle
import seaborn as sns
import datetime as dtm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.svm import SVC
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import joblib

nltk.download('stopwords')

app = Flask(__name__)

# Load data
data_training = pd.read_excel('data_training.xlsx')
data_testing = pd.read_excel('data_testing_label.xlsx')

# Define preprocessing function
def preprocess_text(text):
    #text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    stop_words = set(stopwords.words('indonesian'))
    tokens = [t for t in text.split() if t not in stop_words]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
    return ' '.join(tokens)

# Preprocess data
kronologi_training_preprocessed = [preprocess_text(teks) for teks in data_training['kronologi']]
kronologi_testing_preprocessed = [preprocess_text(teks) for teks in data_testing['kronologi']]

# Memisahkan kronologi dan label dari data training
pasal_1_training = data_training['pasal_1']
pasal_2_training = data_training['pasal_2']

# Membuat vectorizer TF-IDF
vectorizer = TfidfVectorizer()

# Mengubah kronologi training dan testing yang telah diproses menjadi vektor TF-IDF
kronologi_training_vect = vectorizer.fit_transform(kronologi_training_preprocessed)
kronologi_testing_vect = vectorizer.transform(kronologi_testing_preprocessed)

# Memisahkan dataset training dan validasi
X_train, X_val = train_test_split(data_training['kronologi'], test_size=0.2, random_state=42)
y_train, y_val = train_test_split(data_training['pasal_1'], test_size=0.2, random_state=42)
y_train_2, y_val_2 = train_test_split(data_training['pasal_2'], test_size=0.2, random_state=42)

# Menggabungkan data dengan label
data_validation = pd.DataFrame({'kronologi': X_val, 'pasal_1': y_val, 'pasal_2': y_val_2})

# Menyimpan dataset validasi
data_validation.to_csv('data_validation.csv', index=False)

# Define hyperparameter grid
param_grid = {'C': [0.1, 1, 10], 'gamma': [0.01, 0.1, 1]}

# Melatih model RBF SVM dengan cross validation dan grid search
param_grid = {'C': [0.1, 1, 10], 'gamma': [0.01, 0.1, 1]}
cv = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=5)
cv.fit(kronologi_training_vect, pasal_1_training)
best_model_pasal_1 = cv.best_estimator_

# Melatih model RBF SVM dengan cross validation dan grid search
cv = GridSearchCV(SVC(kernel='rbf'), param_grid, cv=5)
cv.fit(kronologi_training_vect, pasal_2_training)
best_model_pasal_2 = cv.best_estimator_

# Memprediksi pasal 1 dan pasal 2 untuk data testing
pasal_1_pred = best_model_pasal_1.predict(kronologi_testing_vect)
pasal_2_pred = best_model_pasal_2.predict(kronologi_testing_vect)

data_testing['pasal_1_prediksi'] = pasal_1_pred
data_testing['pasal_2_prediksi'] = pasal_2_pred

data_testing.to_excel('output.xlsx', index=False)

pasal_1 = data_testing["pasal_1"]  # Assuming "pasal_1" is a column name in your CSV
pasal_1_pred = data_testing["pasal_1_prediksi"]  # Assuming "predicted_pasal_1" is another column
pasal_2 = data_testing["pasal_2"]  # Assuming "pasal_1" is a column name in your CSV
pasal_2_pred = data_testing["pasal_2_prediksi"]  # Assuming "predicted_pasal_1" is another column

def _get_classification_report_pasal_1(pasal_1, pasal_1_pred):
    """Generate classification report"""
    report_pasal_1 = classification_report(pasal_1, pasal_1_pred)
    return report_pasal_1
def _get_classification_report_pasal_2(pasal_2, pasal_2_pred):
    """Generate classification report"""
    report_pasal_2 = classification_report(pasal_2, pasal_2_pred)
    return report_pasal_2
report_pasal_1 = _get_classification_report_pasal_1(pasal_1, pasal_1_pred)
report_pasal_2 = _get_classification_report_pasal_2(pasal_2, pasal_2_pred)



with open('pasal_1_pred.pkl', 'wb') as f:
    pickle.dump((pasal_1_pred), f)
with open('pasal_2_pred.pkl', 'wb') as f:
    pickle.dump((pasal_2_pred), f)

# Save models
joblib.dump(pasal_1_pred, 'best_model_pasal_1.joblib')
joblib.dump(pasal_2_pred, 'best_model_pasal_2.joblib')