import statistics
import pandas as pd
from sklearn.decomposition import PCA
from ansible_collections.cisco.ios.plugins.modules.ios_system import diff_list
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

def standarized_data(data):
    scaler = StandardScaler()
    numeric_data = data.select_dtypes(include=['number'])
    standardized_data = scaler.fit_transform(numeric_data)
    standardized_df = pd.DataFrame(standardized_data, columns=numeric_data.columns)
    standardized_df["knight"] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    return standardized_df

def show_graph(total):
    fig, ax = plt.subplots()
    x = np.arange(1, len(total) + 1)
    ax.plot(x, total)
    ax.set_xlabel('Number of components')
    ax.set_ylabel('Explained Variance Ratio(%)')
    plt.show()

def main():
    try:
        data = pd.read_csv('../Train_knight.csv')
    except FileNotFoundError as e:
        print(f'{e}')
        return

    standarized_df = standarized_data(data)
    if standarized_df.empty:
        print('Error')
        return

    pca = PCA()
    pca.fit_transform(standarized_df)
    explained_variance_ratio = pca.explained_variance_ratio_
    print(explained_variance_ratio)

    total = np.cumsum(explained_variance_ratio) * 100
    print(total)

    show_graph(total)

if __name__ == "__main__":
    main()