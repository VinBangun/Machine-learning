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
            var tableHtml = `
                <h3>Result:</h3>
                <table class="table table-bordered">
                <tr>
                  <th>Kronologi</th>
                  <th>Pasal 1</th>
                  <th>Pasal 2</th>
                </tr>
                <tr>
                  <td>${kronologi}</td>
                  <td>${data.pasal_1}</td>
                  <td>${data.pasal_2}</td>
                </tr>
              </table>
            `;
            resultDiv.innerHTML = tableHtml;
        })
        .catch(error => console.error('Error:', error));
}
