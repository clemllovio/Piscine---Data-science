import sys
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <train_knight.csv> <test_knight.csv>")
        return

    train_knight_path = sys.argv[1]
    test_knight_path = sys.argv[2]

    try:
        train_knight_data = pd.read_csv(train_knight_path)
        test_knight_data = pd.read_csv(test_knight_path)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return

    scaler = StandardScaler()
    numeric_data = train_knight_data.select_dtypes(include=['number'])
    standardized_data = scaler.fit_transform(numeric_data)
    standardized_df = pd.DataFrame(standardized_data, columns=numeric_data.columns)
    standardized_df["knight"] = train_knight_data['knight']

    numeric_data_test = test_knight_data.select_dtypes(include=['number'])
    standardized_data_test = scaler.fit_transform(numeric_data_test)
    standardized_df_test = pd.DataFrame(standardized_data_test, columns=numeric_data.columns)

    X_train = standardized_df.drop(columns=["knight"])
    y_train = standardized_df["knight"]

    X_test = standardized_df_test

    best_k = 0
    best_score = 0
    accuracy_scores = []


    for k in range(2, 31):
        model = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(model, X_train, y_train, cv=5)  # 5-fold cross-validation
        avg_score = scores.mean()
        accuracy_scores.append(avg_score)

        if avg_score > best_score:
            best_score = avg_score
            best_k = k

    plt.plot(range(2, 31), accuracy_scores)
    plt.show()

    final_model = KNeighborsClassifier(n_neighbors=best_k)
    final_model.fit(X_train, y_train)

    y_pred_train = final_model.predict(X_train)
    f1 = f1_score(y_train, y_pred_train, average='weighted')
    print(f"F1-score: {f1:.4f}")
    if f1 < 0.9:
        print("Warning: F1-score is below 90%")

    predictions = final_model.predict(X_test)

    with open("KNN.txt", "w") as f:
        for pred in enumerate(predictions):
            f.write(f"{pred[1]}\n")

if __name__ == "__main__":
    main()