import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
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

    model1 = DecisionTreeClassifier()
    model1.fit(X_train, y_train)
    model2 = LogisticRegression()
    model2.fit(X_train, y_train)

    best_k = 0
    best_score = 0
    accuracy_scores = []
    for k in range(1, 31):
        model3 = KNeighborsClassifier(n_neighbors=k)
        model3.fit(X_train, y_train)
        y_pred_val = model3.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred_val)
        accuracy_scores.append(accuracy)

        if accuracy > best_score:
            best_score = accuracy
            best_k = k
    final_model3 = KNeighborsClassifier(n_neighbors=best_k)
    final_model3.fit(X_train, y_train)

    voting_model = VotingClassifier(estimators=[('dt', model1), ('lr', model2), ('knn', model3)], voting='soft')
    voting_model.fit(X_train, y_train)

    y_prediction_val = voting_model.predict(X_val)
    f1 = f1_score(y_val, y_prediction_val, average='weighted')
    print(f"F1-score (validation): {f1:.4f}")
    if f1 < 0.94:
        print("Warning: F1-score is below 90%")

    predictions = voting_model.predict(X_test)
    predictions = ['Jedi' if pred == 1 else 'Sith' for pred in predictions]
    with open("Voting.txt", "w") as f:
        for pred in predictions:
            f.write(f"{pred}\n")


if __name__ == "__main__":
    main()