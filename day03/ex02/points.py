import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_correlation_matrix(path):
    try:
        data = pd.read_csv(path)

        data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
        numeric_data = data.select_dtypes(include=['number']).dropna()
        correlation = numeric_data.corr()["knight"].abs().sort_values(ascending=False)
        return correlation, data
    except FileNotFoundError:
        print(f'{e}')
        return None, None

def high_correlation_graph(correlation, data, data_test):
    highest_correlation = correlation.index[1]
    second_highest_correlation = correlation.index[2]

    sns.scatterplot(x=data[highest_correlation], y=data[second_highest_correlation],
                    hue=data["knight"], palette={"Sith": "red", "Jedi": "blue"}, alpha=0.5)

    plt.xlabel(highest_correlation)
    plt.ylabel(second_highest_correlation)
    plt.legend()
    plt.show()

    sns.scatterplot(x=data_test[highest_correlation], y=data_test[second_highest_correlation], color='green', label='Knight', alpha=0.5)

    plt.xlabel(highest_correlation)
    plt.ylabel(second_highest_correlation)
    plt.legend()
    plt.show()


def low_correlation_graph(correlation, data, data_test):
    lowest_correlation = correlation.index[-2]
    second_lowest_correlation = correlation.index[-1]

    sns.scatterplot(x=data[lowest_correlation], y=data[second_lowest_correlation],
                hue=data["knight"], palette={"Sith": "red", "Jedi": "blue"}, alpha=0.5)
    plt.xlabel(lowest_correlation)
    plt.ylabel(second_lowest_correlation)
    plt.legend()
    plt.show()

    sns.scatterplot(x=data_test[lowest_correlation], y=data_test[second_lowest_correlation], color='green', label='Knight', alpha=0.5)
    plt.xlabel(lowest_correlation)
    plt.ylabel(second_lowest_correlation)
    plt.legend()
    plt.show()

def main():
    correlation, data = get_correlation_matrix("../Train_knight.csv")
    if correlation.empty or data.empty:
        return

    try:
        data_test = pd.read_csv("../Test_knight.csv")
    except FileNotFoundError:
        print(f'{e}')
        return

    data["knight"] = data["knight"].map({0: "Sith", 1: "Jedi"}).astype(str)
    high_correlation_graph(correlation, data, data_test)
    low_correlation_graph(correlation, data, data_test)

if __name__ == "__main__":
    main()