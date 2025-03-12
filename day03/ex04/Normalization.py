import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
import seaborn as sns


def get_correlation_matrix(data):
    data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    numeric_data = data.select_dtypes(include=['number']).dropna()
    correlation = numeric_data.corr()["knight"].abs().sort_values(ascending=False)
    return correlation


def low_correlation_graph(correlation, data, data_test):
    lowest_correlation = correlation.index[-2]
    second_lowest_correlation = correlation.index[-1]

    sns.scatterplot(x=data[lowest_correlation], y=data[second_lowest_correlation],
                hue=data["knight"], palette={"Sith": "red", "Jedi": "blue"}, alpha=0.5)
    plt.xlabel(lowest_correlation)
    plt.ylabel(second_lowest_correlation)
    plt.legend()
    plt.show()

    sns.scatterplot(x=data_test[lowest_correlation], y=data_test[second_lowest_correlation], color='green',
                    label='Knight', alpha=0.5)
    plt.xlabel(lowest_correlation)
    plt.ylabel(second_lowest_correlation)
    plt.legend()
    plt.show()


def main():
    try:
        data = pd.read_csv('../Train_knight.csv')
        data_test = pd.read_csv('../Test_knight.csv')
    except FileNotFoundError as e:
        print(f'{e}')
        return

    scaler = MinMaxScaler()
    numeric_data = data.select_dtypes(include=['number'])
    normalized_data = scaler.fit_transform(numeric_data)
    normalized_df = pd.DataFrame(normalized_data, columns=numeric_data.columns)
    normalized_df["knight"] = data['knight']

    numeric_data_test = data_test.select_dtypes(include=['number'])
    normalized_data_test = scaler.fit_transform(numeric_data)
    normalized_df_test = pd.DataFrame(normalized_data_test, columns=numeric_data.columns)

    correlation = get_correlation_matrix(normalized_df.copy())
    low_correlation_graph(correlation, normalized_df, normalized_df_test)
    print(normalized_df)


if __name__ == "__main__":
    main()