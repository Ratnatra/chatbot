import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess(data_path):
    df = pd.read_csv(data_path)
    # Example: Assume 'recommendation' is the target
    X = df.drop('recommendation', axis=1)
    y = df['recommendation']
    # Handle missing values (simple strategy)
    X = X.fillna(X.mean(numeric_only=True))
    # One-hot encode categorical columns
    X = pd.get_dummies(X)
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test, scaler, X.columns.tolist()