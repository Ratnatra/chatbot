from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_and_save(X_train, y_train, model_path='model.pkl'):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    joblib.dump(clf, model_path)
    return clf

def evaluate(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {acc:.2f}')
    return acc

if __name__ == "__main__":
    from preprocess import load_and_preprocess
    X_train, X_test, y_train, y_test, scaler, feature_names = load_and_preprocess('../data/patient_data.csv')
    clf = train_and_save(X_train, y_train)
    evaluate(clf, X_test, y_test)
    # Save scaler & feature names for use in the app
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(feature_names, 'features.pkl')