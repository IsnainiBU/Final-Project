import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# 1. Memuat Dataset
data = pd.read_csv("..\german_credit_data.csv")  # Perbarui jalur ke lokasi yang benar

# 2. Menambahkan Kolom Risiko
def determine_risk(row):
    if row['Credit amount'] > 5000 and row['Duration'] > 30:
        return 1
    return 0

data['Risk'] = data.apply(determine_risk, axis=1)

# 3. Penanganan Missing Values
categorical_columns = ['Sex', 'Housing', 'Saving accounts', 'Checking account', 'Purpose']
for column in categorical_columns:
    data[column] = data[column].fillna('Unknown')
    
numerical_columns = ['Age', 'Credit amount', 'Duration']
for column in numerical_columns:
    data[column] = data[column].fillna(data[column].median())

# 4. Preprocessing (Label Encoding untuk kolom kategorikal, kecuali 'Job' karena numerik)
label_encoders = {}
for column in categorical_columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# 5. Fitur dan Target
X = data[['Age', 'Job', 'Sex', 'Housing', 'Saving accounts', 'Checking account', 'Credit amount', 'Duration', 'Purpose']]
y = data['Risk']

# 6. Pembagian Data (Train-Test Split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 7. Standardisasi Fitur
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 8. Train Logistic Regression Model (dengan GridSearchCV untuk hyperparameter tuning)
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.01, 0.1, 1, 10],
    'solver': ['liblinear', 'saga']
}
grid_search = GridSearchCV(LogisticRegression(max_iter=1000), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_scaled, y_train)

# 9. Model Terbaik dan Parameter
print("Best parameters found: ", grid_search.best_params_)
best_model = grid_search.best_estimator_

# 10. Evaluasi Model
y_pred = best_model.predict(X_test_scaled)
print("\n=== Evaluasi Model ===")
print("Akurasi:", accuracy_score(y_test, y_pred))
print("\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred))

# 11. Confusion Matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 12. Menyimpan Model dan Encoder
joblib.dump(best_model, "credit_risk_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model, encoder, dan scaler disimpan dengan sukses!")
