from unittest import result
from flask import Flask, jsonify, redirect, render_template, request, url_for
import pickle
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from flask_paginate import Pagination, get_page_args
from sklearn.svm import SVC
import model as ml

app = Flask(__name__)

#Load the TF-IDF vectorizer
vectorizer = ml.vectorizer


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train():
    if request.method == 'POST':
        file = request.files['file']
        if file:
                df = pd.read_excel(file)
                kronologi_preprocessed = [ml.preprocess_text(teks) for teks in df['kronologi']]
                no = df['no']
                pasal_1 = df['pasal_1']
                pasal_2 = df['pasal_2']
                
                # Menentukan jumlah data yang akan ditampilkan
                num_data = int(request.form.get('num_data', 10))
                kronologi = kronologi_preprocessed[:num_data]
                pasal_1 = pasal_1[:num_data]
                pasal_2 = pasal_2[:num_data]
                
                return render_template('index.html', result='Model trained successfully!', 
                                       kronologi=kronologi, pasal_1=pasal_1, pasal_2=pasal_2, no=no)
        else:
            return render_template('index.html', result='No file uploaded')


@app.route('/test', methods=['POST'])
def test():
    file = request.files['file']
    if file:
        df = pd.read_excel(file)
        # Preprocess the data and extract the kronologi, pasal_1, and pasal_2 columns
        kronologi = [ml.preprocess_text(teks) for teks in df['kronologi']]
        #kronologi= df['kronologi']
        data_training = pd.read_excel('data_training.xlsx')
        data_testing_label= pd.read_excel('data_testing_label.xlsx')
        kronologi_testing = [ml.preprocess_text(teks) for teks in data_testing_label['kronologi']]
        pasal_1_label = data_testing_label['pasal_1']
        pasal_2_label = data_testing_label['pasal_2']
        kronologi_training_preprocessed = [ml.preprocess_text(teks) for teks in data_training['kronologi']]
        pasal_1_training = data_training['pasal_1']
        pasal_2_training = data_training['pasal_2']
        no=df['no']
        pasal_1 = df['pasal_1']
        pasal_2 = df['pasal_2']
        vectorizer = TfidfVectorizer()
        kronologi_training_vect = vectorizer.fit_transform(kronologi_training_preprocessed)
        kronologi_vect = vectorizer.transform(kronologi)
        
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
        pasal_1_pred = best_model_pasal_1.predict(kronologi_vect)
        pasal_2_pred = best_model_pasal_2.predict(kronologi_vect)
        
        def _get_classification_report_pasal_1(pasal_1_label, pasal_1_pred):
            """Generate classification report"""
            report_pasal_1 = classification_report(pasal_1_label, pasal_1_pred, output_dict=True)
            
            # Convert the report to DataFrame
            df_report = pd.DataFrame(report_pasal_1).transpose()

            # Format the 'support' column to have no decimal points
            df_report['support'] = df_report['support'].apply(lambda x: int(x))

            # Format the DataFrame to HTML with specific float formatting
            html_report_pasal_1 = df_report.to_html(classes="table table",
                                                    float_format=lambda x: '{:.2f}'.format(x) if isinstance(x, float) else x,
                                                    justify='center',
                                                    na_rep='')

            # Remove '0' in the 'support' column
            html_report_pasal_1 = html_report_pasal_1.replace('>0<', '><')
            
            return html_report_pasal_1

        def _get_classification_report_pasal_2(pasal_2_label, pasal_2_pred):
            """Generate classification report"""
            report_pasal_2 = classification_report(pasal_2_label, pasal_2_pred, output_dict=True)
            
            # Convert the report to DataFrame
            df_report = pd.DataFrame(report_pasal_2).transpose()

            # Format the 'support' column to have no decimal points
            df_report['support'] = df_report['support'].apply(lambda x: int(x))

            # Format the DataFrame to HTML with specific float formatting
            html_report_pasal_2 = df_report.to_html(classes="table table",
                                                    float_format=lambda x: '{:.2f}'.format(x) if isinstance(x, float) else x,
                                                    justify='center',
                                                    na_rep='')

            # Remove '0' in the 'support' column
            html_report_pasal_2 = html_report_pasal_2.replace('>0<', '><')
            
            return html_report_pasal_2


        report_pasal_1 = _get_classification_report_pasal_1(pasal_1_label, pasal_1_pred)
        report_pasal_2 = _get_classification_report_pasal_2(pasal_2_label, pasal_2_pred)
        
        def _get_confusion_matrices(pasal_1_label, pasal_1_pred, pasal_2_label, pasal_2_pred):
            conf_matrix_pasal_1 = confusion_matrix(pasal_1_label, pasal_1_pred)
            conf_matrix_pasal_2 = confusion_matrix(pasal_2_label, pasal_2_pred)
            return conf_matrix_pasal_1, conf_matrix_pasal_2
        
        conf_matrix_pasal_1, conf_matrix_pasal_2 = _get_confusion_matrices(pasal_1_label, pasal_1_pred, pasal_2_label, pasal_2_pred)

        # Simpan heatmap pasal 1
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix_pasal_1, annot=True, cmap='Blues', fmt='g')
        plt.xlabel('Predicted labels')
        plt.ylabel('Actual')
        plt.savefig('static/conf_matrix_pasal_1.png')  # Simpan sebagai file gambar

        # Simpan heatmap pasal 2
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix_pasal_2, annot=True, cmap='Blues', fmt='g')
        plt.xlabel('Predicted labels')
        plt.ylabel('Actual')
        plt.savefig('static/conf_matrix_pasal_2.png')  # Simpan sebagai file gambar

        heatmap_pasal_1 = sns.heatmap(conf_matrix_pasal_1, annot=True, cmap='Blues', fmt='g')
        heatmap_pasal_1.set_xlabel('Predicted labels')
        heatmap_pasal_1.set_ylabel('Actual')

        heatmap_pasal_2 = sns.heatmap(conf_matrix_pasal_2, annot=True, cmap='Blues', fmt='g')
        heatmap_pasal_2.set_xlabel('Predicted labels')
        heatmap_pasal_2.set_ylabel('Actual')
        
        # Menentukan jumlah data yang akan ditampilkan
        num_data = int(request.form.get('num_data', 10))
        kronologi = kronologi[:num_data]
        pasal_1 = pasal_1[:num_data]
        pasal_2 = pasal_2[:num_data]
        pasal_1_pred = pasal_1_pred[:num_data]
        pasal_2_pred = pasal_2_pred[:num_data]
        kronologi_testing = kronologi_testing[:num_data]
        pasal_1 = pasal_1_label[:num_data]
        pasal_2 = pasal_2_label[:num_data]

        
        return render_template('index.html', result_test='Model testing successfully!', kronologi_testing=kronologi_testing, pasal_1_label=pasal_1_label,
                               pasal_2_label=pasal_2_label,
                               kronologi_test=kronologi, 
                               pasal_1_test=pasal_1, pasal_2_test=pasal_2, no_test=no, 
                               pasal_1_prediksi_test=pasal_1_pred, pasal_2_prediksi_test=pasal_2_pred, 
                               report_pasal_1=report_pasal_1, report_pasal_2=report_pasal_2,
                               conf_matrix_pasal_1=conf_matrix_pasal_1, conf_matrix_pasal_2=conf_matrix_pasal_2, heatmap_pasal_1=heatmap_pasal_1,
                               heatmap_pasal_2=heatmap_pasal_2)
    else:
        return render_template('index.html', result_test='No file uploaded')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if data is None or 'kronologi' not in data:
        return jsonify({'error': 'Invalid input. Please provide "kronologi" field in JSON format.'}), 400
    
    kronologi = data['kronologi']
    if not isinstance(kronologi, str) or kronologi.strip() == '':
        return jsonify({'error': 'Invalid input. "kronologi" must be a non-empty string.'}), 400

    kronologi = ml.preprocess_text(kronologi)
    kronologi_vect = vectorizer.transform([kronologi])
    
    try:
        pasal_1_pred = ml.best_model_pasal_1.predict(kronologi_vect)[0]
        pasal_2_pred = ml.best_model_pasal_2.predict(kronologi_vect)[0]
        return jsonify({'pasal_1': pasal_1_pred, 'pasal_2': pasal_2_pred})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
