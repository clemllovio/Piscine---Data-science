import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_correlation_matrix(data):
    data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    correlation = data.corr()
    return correlation

def main():
    try:
        data = pd.read_csv("../Train_knight.csv")
    except FileNotFoundError as e:
        print(f'{e}')
        return None, None

    correlation = get_correlation_matrix(data)
    if correlation.empty:
        return

    sns.heatmap(correlation, cmap="YlGnBu", annot=False)
    plt.show()

if __name__ == "__main__":
    main()