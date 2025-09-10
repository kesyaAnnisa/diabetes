from flask import Flask, request, jsonify, render_template_string, redirect
import pickle
import mysql.connector
import numpy as np

# ==============================
# Load model Logistic Regression
# ==============================
with open("logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

# Inisialisasi Flask
app = Flask(__name__)

# ==============================
# Koneksi Database
# ==============================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # sesuaikan dengan setting MySQL
        user="root",            # ganti dengan user MySQL kamu
        password="",            # ganti dengan password MySQL kamu
        database="diabetes_db"  # sesuai nama database
    )

# Kolom fitur sesuai model
FEATURE_COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

# ==============================
# ROUTES
# ==============================

# 🔹 Redirect root ke form
@app.route("/")
def home():
    return redirect("/form")

# 🔹 Prediksi dari database berdasarkan ID pasien
@app.route("/predict/<int:patient_id>", methods=["GET"])
def predict_from_db(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return jsonify({"error": "Patient not found"}), 404

    # Ambil fitur sesuai urutan
    features = np.array([row[col] for col in FEATURE_COLUMNS]).reshape(1, -1)
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]

    return jsonify({
        "patient_id": patient_id,
        "input_data": {col: row[col] for col in FEATURE_COLUMNS},
        "prediction": int(prediction),
        "probability_diabetes": float(proba)
    })

# 🔹 Prediksi dengan input manual (JSON)
@app.route("/predict", methods=["POST"])
def predict_manual():
    data = request.json
    try:
        features = np.array([data[col] for col in FEATURE_COLUMNS]).reshape(1, -1)
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400

    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0][1]

    return jsonify({
        "input_data": data,
        "prediction": int(prediction),
        "probability_diabetes": float(proba)
    })

# 🔹 Form input manual via HTML
@app.route("/form", methods=["GET", "POST"])
def form_input():
    if request.method == "POST":
        try:
            data = {col: float(request.form[col]) for col in FEATURE_COLUMNS}
            features = np.array([data[col] for col in FEATURE_COLUMNS]).reshape(1, -1)

            prediction = model.predict(features)[0]
            proba = model.predict_proba(features)[0][1]

            return render_template_string(HTML_FORM, result={
                "input_data": data,
                "prediction": int(prediction),
                "probability_diabetes": round(float(proba), 4)
            })
        except Exception as e:
            return f"Error: {e}", 400

    return render_template_string(HTML_FORM, result=None)

# 🔹 Template HTML sederhana
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Diabetes Prediction</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input { margin: 5px; padding: 8px; width: 200px; }
        button { margin: 10px; padding: 10px 15px; }
        .result { margin-top: 20px; padding: 15px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h2>Form Prediksi Diabetes</h2>
    <form method="post">
        <input type="number" step="any" name="Pregnancies" placeholder="Pregnancies" required><br>
        <input type="number" step="any" name="Glucose" placeholder="Glucose" required><br>
        <input type="number" step="any" name="BloodPressure" placeholder="BloodPressure" required><br>
        <input type="number" step="any" name="SkinThickness" placeholder="SkinThickness" required><br>
        <input type="number" step="any" name="Insulin" placeholder="Insulin" required><br>
        <input type="number" step="any" name="BMI" placeholder="BMI" required><br>
        <input type="number" step="any" name="DiabetesPedigreeFunction" placeholder="DiabetesPedigreeFunction" required><br>
        <input type="number" step="any" name="Age" placeholder="Age" required><br>
        <button type="submit">Prediksi</button>
    </form>

    {% if result %}
        <div class="result">
            <h3>Hasil Prediksi:</h3>
            <p><b>Prediction:</b> {{ result.prediction }}</p>
            <p><b>Probability Diabetes:</b> {{ result.probability_diabetes }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

# ==============================
# RUN SERVER
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4444, debug=True)
