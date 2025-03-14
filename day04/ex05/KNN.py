import sys
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <train_knight.csv> <test_knight.csv>")
        return

    train_knight_path = sys.argv[1]
    test_knight_path = sys.argv[2]

    if not train_knight_path.endswith('.csv') or not test_knight_path.endswith('.csv'):
        print('Usage: python Confusion_Matrix.py <file.csv> <file.csv>')
        return

    try:
        train_knight_data = pd.read_csv(train_knight_path)
        test_knight_data = pd.read_csv(test_knight_path)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    scaler = StandardScaler()

    train_knight_data['knight'] = train_knight_data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    train_knight_data, validation_data = train_test_split(train_knight_data, test_size=0.3, random_state=42)

    X_train = train_knight_data.drop(columns=["knight"])
    y_train = train_knight_data["knight"]

    X_val = validation_data.drop(columns=["knight"])
    y_val = validation_data["knight"]

    scaler.fit(X_train)
    X_train = pd.DataFrame(scaler.transform(X_train), columns=X_train.columns)
    X_val = pd.DataFrame(scaler.transform(X_val), columns=X_val.columns)
    X_test = pd.DataFrame(scaler.transform(test_knight_data), columns=test_knight_data.columns)

    best_k = 0
    best_score = 0
    accuracy_scores = []

    for k in range(1, 31):
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        y_pred_val = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred_val)
        accuracy_scores.append(accuracy)

        if accuracy > best_score:
            best_score = accuracy
            best_k = k

    plt.plot(range(1, 31), accuracy_scores)
    plt.show()

    final_model = KNeighborsClassifier(n_neighbors=best_k)
    final_model.fit(X_train, y_train)

    y_prediction_val = final_model.predict(X_val)
    f1 = f1_score(y_val, y_prediction_val, average='weighted')
    print(f"F1-score (validation): {f1:.4f}")
    if f1 < 0.92:
        print("Warning: F1-score is below 92%")

    predictions = final_model.predict(X_test)
    predictions = ['Jedi' if pred == 1 else 'Sith' for pred in predictions]

    with open("KNN.txt", "w") as f:
        for pred in enumerate(predictions):
            f.write(f"{pred[1]}\n")

if __name__ == "__main__":
    main()