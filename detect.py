from flask import Flask, request
import numpy as np
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Generate sample dataset
np.random.seed(42)

X = np.random.randint(0, 10, size=(200, 34))
y = np.array([0] * 100 + [1] * 100)

# Train model
dt_model = DecisionTreeClassifier()
dt_model.fit(X, y)

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Android Malware Detection</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background: linear-gradient(to right, #141e30, #243b55);
            color: white;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}

        form {{
            background: white;
            color: black;
            padding: 20px;
            border-radius: 10px;
            max-width: 700px;
            margin: auto;
        }}

        .features {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .features div {{
            display: flex;
            flex-direction: column;
        }}

        input[type=number] {{
            width: 70px;
            padding: 5px;
        }}

        button {{
            margin-top: 20px;
            padding: 10px 20px;
            background: #243b55;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}

        button:hover {{
            background: #141e30;
        }}

        .result {{
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
        }}

        .safe {{
            background: #c8f7c5;
            color: green;
        }}

        .danger {{
            background: #ffcccc;
            color: red;
        }}

    </style>
</head>

<body>

    <h1>Android Malware Detection Prototype</h1>

    <form method="POST">

        <div class="features">
            {inputs}
        </div>

        <button type="submit">Predict</button>

        {result_block}

    </form>

</body>
</html>
"""

# Generate 34 input fields
input_fields = "".join([
    f'''
    <div>
        <label>F{i}</label>
        <input type="number" name="f{i}" min="0" max="10" required>
    </div>
    '''
    for i in range(1, 35)
])

@app.route("/", methods=["GET", "POST"])
def home():

    result_block = ""

    if request.method == "POST":

        try:
            # Read inputs
            features = [
                int(request.form[f"f{i}"])
                for i in range(1, 35)
            ]

            # Convert to array
            features_array = np.array(features).reshape(1, -1)

            # Predict
            prediction = dt_model.predict(features_array)[0]

            # Display result
            if prediction == 1:
                result_block = '''
                <div class="result danger">
                    Malicious App Detected 🚨
                </div>
                '''
            else:
                result_block = '''
                <div class="result safe">
                    Benign App ✅
                </div>
                '''

        except Exception as e:

            result_block = f'''
            <div class="result danger">
                Error: {e}
            </div>
            '''

    return html_template.format(
        inputs=input_fields,
        result_block=result_block
    )

if __name__ == "__main__":
    app.run(debug=True)