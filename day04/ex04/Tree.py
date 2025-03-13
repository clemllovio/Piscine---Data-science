import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.metrics import f1_score
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

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    f1 = f1_score(y_train, y_pred_train, average='weighted')
    print(f"F1-score: {f1:.4f}")
    if f1 < 0.9:
        print("Warning: F1-score is below 90%")

    plt.figure(figsize=(20, 10))
    tree.plot_tree(model, feature_names=X_train.columns, class_names=label_encoder.classes_, filled=True)
    plt.savefig("tree.png")
    plt.close()

    predictions = model.predict(X_test)
    predictions = label_encoder.inverse_transform(predictions)
    with open("Tree.txt", "w") as f:
        for pred in predictions:
            f.write(f"{pred}\n")


if __name__ == "__main__":
    main()

