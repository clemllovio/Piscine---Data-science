import pandas as pd
import matplotlib.pyplot as plt

def visualize_knight_data():
    data = pd.read_csv('../Test_knight.csv')

    num_columns = len(data.columns)
    num_rows = (num_columns + 4) // 5

    fig, axes = plt.subplots(num_rows, 5, figsize=(8, 4 * num_rows))

    axes = axes.flatten()

    for i, column in enumerate(data.columns):
        axes[i].hist(data[column], color='#8DBD85')
        axes[i].set_title(f'{column}')
        axes[i].legend('Knight')

    plt.tight_layout()

    plt.show()

def understand_interaction():
    data = pd.read_csv('../Train_knight.csv')

    features = data.columns.difference(['knight'])

    num_features = len(features)
    num_rows = (num_features + 4) // 5
    fig, axes = plt.subplots(num_rows, 5, figsize=(15, num_rows * 4))

    axes = axes.flatten()

    for i, feature in enumerate(features):
        ax = axes[i]

        ax.hist(data[data['knight'] == 'Jedi'][feature], alpha=0.3, color='blue', label='Jedi')
        ax.hist(data[data['knight'] == 'Sith'][feature], alpha=0.3, color='red', label='Sith')

        ax.set_title(f'{feature}')
        ax.legend()

    plt.tight_layout()

    plt.show()

def main():
    visualize_knight_data()
    understand_interaction()

if __name__ == "__main__":
    main()