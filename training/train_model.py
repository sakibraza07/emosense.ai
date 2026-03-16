import numpy as np
from sklearn.model_selection import train_test_split

# Step 1: Load features and labels
features = np.load("features.npy")
labels = np.load("labels.npy")

# Step 2: Split into train (80%) and test (20%)
X_train, X_test, y_train, y_test = train_test_split(
    features,
    labels,
    test_size=0.2,
    random_state=42
)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
from sklearn.neural_network import MLPClassifier

classifier = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=10000, random_state=42)
classifier.fit(X_train, y_train)

accuracy = classifier.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)
import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(classifier, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model and scaler saved.")