from flask import Flask, request, jsonify
import numpy as np
import joblib
import logging

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Muat model, label encoders, dan scaler
model = joblib.load("credit_risk_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
scaler = joblib.load("scaler.pkl")  # Jika model memerlukan scaling

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Ambil data dari request JSON
        data = request.json
        logging.debug(f"Received data: {data}")

        # Validasi input: Semua kolom harus ada
        required_fields = ['Age', 'Job', 'Sex', 'Housing', 'Saving accounts', 
                           'Checking account', 'Credit amount', 'Duration', 'Purpose']
        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field: {field}")
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Encode categorical features menggunakan label encoders, kecuali 'Job'
        encoded_data = {}
        for column in ['Sex', 'Housing', 'Saving accounts', 'Checking account', 'Purpose']:
            try:
                encoded_value = label_encoders[column].transform([data[column]])[0]
                encoded_data[column] = encoded_value
            except ValueError:
                logging.warning(f"Unknown value '{data[column]}' for column '{column}'. Defaulting to 'Unknown'.")
                if 'Unknown' in label_encoders[column].classes_:
                    encoded_value = label_encoders[column].transform(['Unknown'])[0]
                else:
                    encoded_value = label_encoders[column].transform([label_encoders[column].classes_[0]])[0]
                encoded_data[column] = encoded_value

        # 'Job' dianggap sebagai numerik
        try:
            job_value = int(data["Job"])
        except ValueError:
            logging.error("Invalid value for 'Job', expected an integer.")
            return jsonify({"error": "Invalid value for 'Job', expected an integer."}), 400

        # Buat array fitur untuk prediksi
        features = np.array([
            data["Age"], job_value, encoded_data['Sex'], encoded_data['Housing'], 
            encoded_data['Saving accounts'], encoded_data['Checking account'], 
            data["Credit amount"], data["Duration"], encoded_data['Purpose']
        ]).reshape(1, -1)

        # Transformasi fitur numerik jika model memerlukan scaler
        features_scaled = scaler.transform(features)

        # Prediksi risiko menggunakan model
        prediction = model.predict(features_scaled)
        risk = "low" if prediction[0] == 0 else "high"

        # Prediksi probabilitas
        probabilities = model.predict_proba(features_scaled)
        risk_prob = probabilities[0][1]  # Probabilitas untuk risiko tinggi

        # Log hasil prediksi
        logging.info(f"Prediction result: {risk}, Probability: {risk_prob}")

        # Kembalikan hasil prediksi dan probabilitas sebagai JSON
        return jsonify({"risk": risk, "probability": risk_prob})

    except KeyError as e:
        logging.error(f"Missing required field: {str(e)}")
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        logging.error(f"Value error: {str(e)}")
        return jsonify({"error": f"Value error: {str(e)}"}), 400
    except Exception as e:
        logging.exception("An error occurred during prediction.")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Jalankan aplikasi Flask di localhost pada port 5000
    app.run(debug=True)
