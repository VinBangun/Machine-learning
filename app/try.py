@app.route('/training', methods=['GET', 'POST'])
def training():
    if request.method == 'POST':
        file = request.files['file']
        data = pd.read_excel(file)
        kronologi = data['kronologi']
        kronologi = ml.pre_processing(kronologi)
        kronologi_split = ml.train_test_split(kronologi)
        kronologi_vect = ml.vectorizer.fit_transform[(kronologi_split)]
        pasal_1 = data['pasal_1']
        pasal_2 = data['pasal_2']
        pasal_1_pred = ml.best_model_pasal_1.predict(kronologi_vect)
        pasal_2_pred = ml.best_model_pasal_2.predict(kronologi_vect)

@app.route('/train', methods=['POST'])
def train():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Example code assuming CSV file format
        df = pd.read_excel(file)
        kronologi = ml.preprocess_text(df)
        kronologi_train = [ml.preprocess_text(teks) for teks in kronologi['kronologi']]
        training_result = kronologi_train
        # Assume pasal_1 and pasal_2 are extracted from the training data
        pasal_1 = "Pasal 1 result"
        pasal_2 = "Pasal 2 result"
        
        # Save the result of the training
        training_result = "Training completed successfully"
    except Exception as e:
        training_result = str(e)
        pasal_1 = ""
        pasal_2 = ""
    
    # Return the result to index.html
    return render_template('index.html', result=training_result, data={"pasal_1": pasal_1, "pasal_2": pasal_2})
        
        
        #@app.route('/test', methods=['POST'])
#def test():
    file = request.files['file']
    if file:
        df = pd.read_excel(file)
        # Preprocess the data and extract the kronologi, pasal_1, and pasal_2 columns
        kronologi_preprocessed = [ml.preprocess_text(teks) for teks in df['kronologi']]
        no=df['no']
        pasal_1 = df['pasal_1']
        pasal_2 = df['pasal_2']
        vectorizer = TfidfVectorizer()
        kronologi_training_vect = vectorizer.fit_transform(kronologi_preprocessed)
        
        # Define parameters for GridSearchCV
        param_grid = {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}
        
        # Train models
        best_model_pasal_1, best_model_pasal_2 = test_model(kronologi_training_vect, pasal_1, pasal_2, param_grid)
        
        #pasal_1_pred = best_model_pasal_1.predict(kronologi_training_vect)[0]
        #pasal_2_pred = best_model_pasal_2.predict(kronologi_training_vect)[0]
        
        return render_template('index.html', result_test='Model testing successfully!', kronologi=kronologi_preprocessed,pasal_1=pasal_1, pasal_2=pasal_2, no=no,pasal_1_prediksi=best_model_pasal_1, pasal_2_prediksi=best_model_pasal_2)
    else:
        return render_template('index.html', result_test='No file uploaded')

#def test_model(X, y1, y2, param_grid, kernel='rbf', cv=5):
    cv = GridSearchCV(SVC(kernel=kernel), param_grid, cv=cv)
    cv.fit(X, y1)
    best_model_pasal_1 = cv.best_estimator_
    
    cv = GridSearchCV(SVC(kernel=kernel), param_grid, cv=cv)
    cv.fit(X, y2)
    best_model_pasal_2 = cv.best_estimator_
    
    return best_model_pasal_1, best_model_pasal_2




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Program Tugas Akhir</title>
</head>
<body>
    <section></section>
    <h1>Training</h1>
    <form action="/train" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xlsx, .xls">
        <button type="submit">Upload</button>
    </form>

    {% if result %}
        <p>{{ result }}</p>
    {% endif %}

    {% if no,kronologi,pasal_1,pasal_2 %}
        <h2>Hasil Proses</h2>
        <table border="1">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Kronologi Preprocessed</th>
                    <th>Pasal 1</th>
                    <th>Pasal 2</th>
                </tr>
            </thead>
            <tbody>
                {% for i in range(kronologi|length) %}
                    <tr>
                        <td>{{ no[i] }}</td>
                        <td>{{ kronologi[i] }}</td>
                        <td>{{ pasal_1[i]  }}</td>
                        <td>{{ pasal_2[i]  }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}
    </section>
    <section>
    <h1>Model Testing</h1>
    <form action="/test" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xlsx">
        <button type="submit">Upload File</button>
    </form>
    {% if result_test %}
        <p>{{ result_test }}</p>
    {% endif %}

    {% if no_test,kronologi_test,pasal_1_test,pasal_2_test,pasal_1_prediksi_test,pasal_2_prediksi_test %}
        <h2>Hasil Proses</h2>
        <table border="1">
            <thead>
                <tr>
                    <th>No</th>
                    <th>Kronologi Preprocessed</th>
                    <th>Pasal 1</th>
                    <th>Pasal 2</th>
                    <th>Pasal 1 Prediksi</th>
                    <th>Pasal 2 Prediksi</th>
                </tr>
            </thead>
            <tbody>
                {% for i in range(kronologi_test|length) %}
                    <tr>
                        <td>{{ no_test[i] }}</td>
                        <td>{{ kronologi_test[i] }}</td>
                        <td>{{ pasal_1_test[i]  }}</td>
                        <td>{{ pasal_2_test[i]  }}</td>
                        <td>{{ pasal_1_prediksi_test[i] }}</td>
                        <td>{{ pasal_2_prediksi_test[i] }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% endif %}

    <h1>Crime Prediction</h1>
    <form id="prediction-form">
        <label for="kronologi">Kronologi:</label><br>
        <textarea id="kronologi" name="kronologi" rows="4" cols="50"></textarea><br><br>
        <button type="button" onclick="predict()">Predict</button>
    </form>
    <div id="prediction-result"></div>

    <script>
        function predict() {
            var kronologi = document.getElementById("kronologi").value;
            var data = { "kronologi": kronologi };

            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById("prediction-result");
                resultDiv.innerHTML = "<p>Pasal 1: " + data.pasal_1 + "</p>";
                resultDiv.innerHTML += "<p>Pasal 2: " + data.pasal_2 + "</p>";
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>


page = int(request.args.get('page', 1))
    page_test = int(request.args.get('page_test', 1))
    limit = 10

    # Calculate offsets
    offset = (page - 1) * limit
    offset_test = (page_test - 1) * limit

    # Train and test data
    train_data = train(offset,limit)
    test_data = test(offset_test, limit)

    # Extract data from train and test results
    no, kronologi, pasal_1, pasal_2 = train_data
    no_test, kronologi_test, pasal_1_test, pasal_2_test, pasal_1_prediksi_test, pasal_2_prediksi_test = test_data

    # Calculate total pages
    total_pages = train(limit)[0] // limit + 1
    total_pages_test = test(limit)[0] // limit + 1

    # Render template
    return render_template('index.html', **{
        'no': no, 'kronologi': kronologi, 'pasal_1': pasal_1, 'pasal_2': pasal_2,
        'no_test': no_test, 'kronologi_test': kronologi_test, 'pasal_1_test': pasal_1_test, 'pasal_2_test': pasal_2_test,
        'pasal_1_prediksi_test': pasal_1_prediksi_test, 'pasal_2_prediksi_test': pasal_2_prediksi_test,
        'page': page, 'total_pages': total_pages,
        'page_test': page_test, 'total_pages_test': total_pages_test
    })
    
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Program Tugas Akhir</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        section {
            background-color: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            margin-bottom: 20px;
        }
        h1 {
            margin-top: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f0f0f0;
        }
       .pagination {
            margin-top: 20px;
            text-align: center;
        }
       .pagination a {
            color: #337ab7;
            text-decoration: none;
        }
       .pagination a:hover {
            color: #23527c;
        }
    </style>
</head>
<body>
    <section>
        <h1>Training</h1>
        <form action="/train" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".xlsx,.xls">
            <button type="submit">Upload</button>
        </form>

        {% if result %}
            <p>{{ result }}</p>
        {% endif %}

        {% if no,kronologi,pasal_1,pasal_2 %}
            <h2>Hasil Proses</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>No</th>
                        <th>Kronologi Preprocessed</th>
                        <th>Pasal 1</th>
                        <th>Pasal 2</th>
                    </tr>
                </thead>
                <tbody>
                    {% for i in range(kronologi|length) %}
                        <tr>
                            <td>{{ no[i] }}</td>
                            <td>{{ kronologi[i] }}</td>
                            <td>{{ pasal_1[i]  }}</td>
                            <td>{{ pasal_2[i]  }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="pagination">
                {% if page > 1 %}
                    <a href="?page={{ page - 1 }}">Previous</a>
                {% endif %}
                Page {{ page }} of {{ total_pages }}
                {% if page < total_pages %}
                    <a href="?page={{ page + 1 }}">Next</a>
                {% endif %}
            </div>
        {% endif %}
    </section>

    <section>
        <h1>Model Testing</h1>
        <form action="/test" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".xlsx">
            <button type="submit">Upload File</button>
        </form>
        {% if result_test %}
            <p>{{ result_test }}</p>
        {% endif %}

        {% if no_test,kronologi_test,pasal_1_test,pasal_2_test,pasal_1_prediksi_test,pasal_2_prediksi_test %}
            <h2>Hasil Proses</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>No</th>
                        <th>Kronologi Preprocessed</th>
                        <th>Pasal 1</th>
                        <th>Pasal 2</th>
                        <th>Pasal 1 Prediksi</th>
                        <th>Pasal 2 Prediksi</th>
                    </tr>
                </thead>
                <tbody>
                    {% for i in range(kronologi_test|length) %}
                        <tr>
                            <td>{{ no_test[i] }}</td>
                            <td>{{ kronologi_test[i] }}</td>
                            <td>{{ pasal_1_test[i]  }}</td>
                            <td>{{ pasal_2_test[i]  }}</td>
                            <td>{{ pasal_1_prediksi_test[i] }}</td>
                            <td>{{ pasal_2_prediksi_test[i] }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="pagination">
                {% if page_test > $@$v=v1.16$@$1 %}
                    <a href="?page_test={{ page_test - 1 }}">Previous</a>
                {% endif %}
                Page {{ page_test }} of {{ total_pages_test }}
                {% if page_test < total_pages_test %}
                    <a href="?page_test={{ page_test + 1 }}">Next</a>
                {% endif %}
            </div>
        {% endif %}
    </section>

    <section>
        <h1>Crime Prediction</h1>
        <form id="prediction-form">
            <label for="kronologi">Kronologi:</label><br>
            <textarea id="kronologi" name="kronologi" rows="4" cols="50"></textarea><br><br>
            <button type="button" onclick="predict()">Predict</button>
        </form>
        <div id="prediction-result"></div>
    </section>

    <script>
        function predict() {
            var kronologi = document.getElementById("kronologi").value;
            var data = { "kronologi": kronologi };

            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById("prediction-result");
                resultDiv.innerHTML = "<p>Pasal 1: " + data.pasal_1 + "</p>";
                resultDiv.innerHTML += "<p>Pasal 2: " + data.pasal_2 + "</p>";
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>