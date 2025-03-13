import pandas as pd
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
import seaborn as sns

def get_correlation_matrix(data):
    try:
        data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
        correlation = data.corr()["knight"].abs().sort_values(ascending=False)
        return correlation
    except FileNotFoundError:
        print(f'{e}')
        return None

def high_correlation_graph(correlation, data, data_test):
    highest_correlation = correlation.index[1]
    second_highest_correlation = correlation.index[2]

    sns.scatterplot(x=data[highest_correlation], y=data[second_highest_correlation],
                    hue=data["knight"], palette={"Sith": "red", "Jedi": "blue"}, alpha=0.5)

    plt.xlabel(highest_correlation)
    plt.ylabel(second_highest_correlation)
    plt.legend()
    plt.show()

    sns.scatterplot(x=data_test[highest_correlation], y=data_test[second_highest_correlation], color='green',
                    label='Knight', alpha=0.5)

    plt.xlabel(highest_correlation)
    plt.ylabel(second_highest_correlation)
    plt.legend()
    plt.show()


def main():
    try:
        data = pd.read_csv('../Train_knight.csv')
        data_test = pd.read_csv('../Test_knight.csv')
    except FileNotFoundError as e:
        print(f'{e}')
        return

    scaler = StandardScaler()
    numeric_data = data.select_dtypes(include=['number'])
    standardized_data = scaler.fit_transform(numeric_data)
    standardized_df = pd.DataFrame(standardized_data, columns=numeric_data.columns)
    standardized_df["knight"] = data['knight']

    numeric_data_test = data_test.select_dtypes(include=['number'])
    standardized_data_test = scaler.fit_transform(numeric_data_test)
    standardized_df_test = pd.DataFrame(standardized_data_test, columns=numeric_data.columns)

    correlation = get_correlation_matrix(standardized_df.copy())
    if correlation is None:
        return
    high_correlation_graph(correlation, standardized_df, standardized_df_test)
    print(standardized_df)

if __name__ == "__main__":
    main()