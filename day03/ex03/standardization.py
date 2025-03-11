import pandas as pd
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
import seaborn as sns

def get_correlation_matrix(data):
    data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    numeric_data = data.select_dtypes(include=['number']).dropna()
    correlation = numeric_data.corr()["knight"].abs().sort_values(ascending=False)
    return correlation

def high_correlation_graph(correlation, data):
    highest_correlation = correlation.index[1]
    second_highest_correlation = correlation.index[2]

    sns.scatterplot(x=data[highest_correlation], y=data[second_highest_correlation],
                    hue=data["knight"], palette={"Sith": "red", "Jedi": "blue"}, alpha=0.5)

    plt.xlabel(highest_correlation)
    plt.ylabel(second_highest_correlation)
    plt.legend()
    plt.show()


def main():
    data = pd.read_csv('../Train_knight.csv')

    scaler = StandardScaler()
    numeric_data = data.select_dtypes(include=['number'])
    standardized_data = scaler.fit_transform(numeric_data)
    standardized_df = pd.DataFrame(standardized_data, columns=numeric_data.columns)

    standardized_df["knight"] = data['knight']

    correlation = get_correlation_matrix(standardized_df.copy())
    high_correlation_graph(correlation, standardized_df)
    print(standardized_df)


if __name__ == "__main__":
    main()