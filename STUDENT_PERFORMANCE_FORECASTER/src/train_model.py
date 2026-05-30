import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

def main():
    print("Starting Model Training Pipeline...")
    
    # 1. Load Data
    data_path = "data/ultimate_student_metrics_30k.csv"
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return
        
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    # 2. Feature Selection
    # Select predictor variables (X) and target variable (y)
    features = ['Study_Hours_Daily', 'Sleep_Hours_Daily', 'Phone_Usage_Hours_Daily']
    target = 'Exam_Score'
    
    X = df[features]
    y = df[target]
    
    # 3. Train/Test Split
    print("Splitting data into training and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Initialize and Train Model
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate Model
    print("Evaluating Model...")
    predictions = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared Score: {r2:.4f}")
    
    # 6. Save Model
    models_dir = "models"
    if not os.path.exists(models_dir):
        print(f"Creating directory: {models_dir}")
        os.makedirs(models_dir)
        
    model_path = os.path.join(models_dir, "student_rf_model.pkl")
    print(f"Saving trained model to {model_path}...")
    
    # Compress=3 shrinks the 190MB model down to around ~5MB!
    joblib.dump(model, model_path, compress=3)
    
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()