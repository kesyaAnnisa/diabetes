from flask import Flask, request, render_template_string, redirect
import pickle
import numpy as np

# ==============================
# Load model Logistic Regression
# ==============================
with open("logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# Kolom fitur sesuai model
FEATURE_COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

# ==============================
# Helper function
# ==============================
def interpret_prediction(pred):
    return "Diabetes" if pred == 1 else "Tidak Diabetes"

# ==============================
# History prediksi
# ==============================
history = []

# ==============================
# HTML Template
# ==============================
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Diabetes Prediction</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: flex-start; min-height: 100vh; margin:0; padding: 20px;}
        .container { background: #fff; padding: 40px 30px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); width: 400px; margin-bottom: 50px;}
        h2 { text-align: center; color: #333; margin-bottom: 20px;}
        input, select { width: 100%; padding: 10px; margin-bottom: 12px; border-radius: 6px; border: 1px solid #ccc; font-size: 14px;}
        button { width: 100%; padding: 12px; border: none; border-radius: 6px; background-color: #4A90E2; color: white; font-size: 16px; cursor: pointer;}
        button:hover { background-color: #357ABD;}
        .result { margin-top: 15px; padding: 15px; border-radius: 8px; background-color: #E8F0FE; color: #333;}
        .history { margin-top: 30px; }
        .history h3 { margin-bottom: 10px; }
        .history ul { padding-left: 20px; }
    </style>
    <script>
        function togglePregnancies() {
            var pernah = document.getElementById("ever_pregnant").value;
            var pregInput = document.getElementById("Pregnancies_input");
            if(pernah === "yes") {
                pregInput.style.display = "block";
            } else {
                pregInput.style.display = "none";
                document.getElementById("Pregnancies").value = 0;
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>Prediksi Diabetes</h2>
        <form method="post">
            <input type="text" name="name" placeholder="Nama Pasien" required>
            
            <label>Pernah hamil?</label>
            <select id="ever_pregnant" name="ever_pregnant" onchange="togglePregnancies()" required>
                <option value="">--Pilih--</option>
                <option value="yes">Ya</option>
                <option value="no">Tidak</option>
            </select>
            
            <div id="Pregnancies_input" style="display:none;">
                <input type="number" step="1" name="Pregnancies" id="Pregnancies" placeholder="Jumlah kehamilan">
            </div>
            
            {% for col in columns if col != "Pregnancies" %}
            <input type="number" step="any" name="{{ col }}" placeholder="{{ col }}" required>
            {% endfor %}
            
            <button type="submit">Prediksi</button>
        </form>

        {% if result %}
            <div class="result">
                <h3>Hasil Prediksi:</h3>
                <p><b>Nama:</b> {{ result.name }}</p>
                <p><b>Prediction:</b> {{ result.prediction }}</p>
                <p><b>Probability Diabetes:</b> {{ result.probability_diabetes }}</p>
            </div>
        {% endif %}
        
        {% if history %}
        <div class="history">
            <h3>History Prediksi:</h3>
            <ul>
                {% for h in history %}
                <li>{{ h.name }} - {{ h.prediction }} (Prob: {{ h.probability_diabetes }})</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# ==============================
# Route Form
# ==============================
@app.route("/form", methods=["GET","POST"])
def form_input():
    result = None
    global history
    if request.method == "POST":
        try:
            # Ambil nama
            name = request.form.get("name", "Unknown")
            
            # Pregnancies
            pernah_hamil = request.form.get("ever_pregnant")
            pregnancies = 0.0
            if pernah_hamil == "yes":
                pregnancies = float(request.form.get("Pregnancies", 0))
            
            # Ambil fitur lain
            data = {"Pregnancies": pregnancies}
            for col in FEATURE_COLUMNS:
                if col != "Pregnancies":
                    data[col] = float(request.form.get(col, 0))  # default 0 supaya aman
            
            # Prediksi
            features = np.array([data[col] for col in FEATURE_COLUMNS]).reshape(1,-1)
            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0][1]
            
            # Hasil
            result = {
                "name": name,
                "prediction": interpret_prediction(prediction),
                "probability_diabetes": round(float(proba),4)
            }
            
            # Simpan history 10 terakhir
            history.insert(0, result)
            if len(history) > 10:
                history = history[:10]
            
        except Exception as e:
            return f"Error: {e}",400
    
    return render_template_string(HTML_FORM, result=result, columns=FEATURE_COLUMNS, history=history)

# ==============================
# Root redirect
# ==============================
@app.route("/")
def home():
    return redirect("/form")

# ==============================
# Run server
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444, debug=True)
