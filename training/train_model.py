"""
Trains and compares several models with stratified k-fold cross-validation
(instead of trusting a single 80/20 split), picks the best one, tunes it,
and saves model.pkl + scaler.pkl in the same format the app already expects
(services/emotion_service.py does model.predict() then maps the code to a
label — no serving-side changes needed as long as you keep using a
scikit-learn-style classifier here).

Run this AFTER preprocessing.py has produced features.npy / labels.npy.
"""
import pickle
import numpy as np
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
)
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

RANDOM_STATE = 42

def main():
    features = np.load("features.npy")
    labels = np.load("labels.npy")

    # Held-out test set the models never see during CV/tuning.
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=RANDOM_STATE, stratify=labels
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    candidates = {
        "MLP": MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=10000,
                              random_state=RANDOM_STATE),
        "SVM_RBF": SVC(kernel="rbf", C=10, gamma="scale", random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=400, random_state=RANDOM_STATE),
    }

    print("=== 5-fold cross-validation on training set ===")
    cv_scores = {}
    for name, model in candidates.items():
        scores = cross_val_score(model, X_train_s, y_train, cv=cv, n_jobs=-1)
        cv_scores[name] = scores.mean()
        print(f"{name}: {scores.mean()*100:.2f}% (+/- {scores.std()*100:.2f}%)")

    best_name = max(cv_scores, key=cv_scores.get)
    print(f"\nBest candidate by CV: {best_name}")

    # Light hyperparameter search around the winner. Keeping grids small so
    # this stays runnable on a laptop.
    param_grids = {
        "MLP": {
            "hidden_layer_sizes": [(256, 128), (128, 64), (256, 128, 64)],
            "alpha": [0.0001, 0.001, 0.01],
        },
        "SVM_RBF": {
            "C": [1, 10, 50],
            "gamma": ["scale", 0.01, 0.001],
        },
        "RandomForest": {
            "n_estimators": [300, 500, 800],
            "max_depth": [None, 20, 40],
        },
    }

    print(f"\n=== Grid search on {best_name} ===")
    grid = GridSearchCV(candidates[best_name], param_grids[best_name],
                         cv=cv, n_jobs=-1, scoring="accuracy")
    grid.fit(X_train_s, y_train)
    print("Best params:", grid.best_params_)
    print(f"Best CV accuracy: {grid.best_score_*100:.2f}%")

    best_model = grid.best_estimator_
    test_accuracy = accuracy_score(y_test, best_model.predict(X_test_s))
    print(f"\n=== Held-out test accuracy: {test_accuracy*100:.2f}% ===")
    print(classification_report(y_test, best_model.predict(X_test_s)))

    with open("model.pkl", "wb") as f:
        pickle.dump(best_model, f)
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print("\nSaved model.pkl and scaler.pkl")


if __name__ == "__main__":
    main()