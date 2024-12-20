import logging
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Muat model dan encoder
model = joblib.load("credit_risk_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Data input yang dimodifikasi untuk memastikan risiko tinggi
data = {
    "Age": 35,
    "Job": 2,  # Asumsikan 1: Unskilled, 2: Skilled, dst.
    "Sex": "male",
    "Housing": "own",
    "Saving accounts": "little",
    "Checking account": "moderate",
    "Credit amount": 10000,  # Jumlah kredit yang lebih tinggi
    "Duration": 36,  # Durasi lebih panjang
    "Purpose": "radio"  # Pastikan kategori ini lebih berisiko, misalnya "radio"
}

# Fitur yang diperlukan
required_fields = ['Age', 'Job', 'Sex', 'Housing', 'Saving accounts', 
                   'Checking account', 'Credit amount', 'Duration', 'Purpose']

for field in required_fields:
    if field not in data:
        logging.error(f"Missing field: {field}")
        raise ValueError(f"Missing field: {field}")

# Encode categorical features dengan penanganan untuk nilai yang tidak dikenal
encoded_data = {}
for column in ['Sex', 'Housing', 'Saving accounts', 'Checking account', 'Purpose']:
    try:
        # Coba encode nilai input
        encoded_value = label_encoders[column].transform([data[column]])[0]
        encoded_data[column] = encoded_value
    except ValueError:
        # Cek apakah nilai sudah ada dalam kategori label, jika tidak, gunakan kategori yang valid
        if data[column] not in label_encoders[column].classes_:
            logging.warning(f"Unknown value '{data[column]}' for column '{column}'. Using a default value.")
            # Gunakan kategori pertama dalam kelas yang ada sebagai fallback
            encoded_value = label_encoders[column].transform([label_encoders[column].classes_[0]])[0]
        else:
            encoded_value = label_encoders[column].transform([data[column]])[0]
        encoded_data[column] = encoded_value

# Lakukan prediksi menggunakan model (gunakan scaler jika perlu)
features = np.array([
    data["Age"], data["Job"], encoded_data['Sex'], encoded_data['Housing'],
    encoded_data['Saving accounts'], encoded_data['Checking account'],
    data["Credit amount"], data["Duration"], encoded_data['Purpose']
]).reshape(1, -1)

# Jika model menggunakan scaler, lakukan transformasi
scaler = joblib.load("scaler.pkl")
features_scaled = scaler.transform(features)

# Prediksi
prediction = model.predict(features_scaled)
risk = "low" if prediction[0] == 0 else "high"

# Prediksi probabilitas
probabilities = model.predict_proba(features_scaled)
risk_prob = probabilities[0][1]  # Probabilitas untuk risiko tinggi

print(f"Prediksi Risiko: {risk}")
print(f"Probabilitas Risiko Tinggi: {risk_prob}")
