import pandas as pd
import matplotlib.pyplot as plt

def visualize_knight_data():
    try:
        data = pd.read_csv('../Test_knight.csv')

        fig, axes = plt.subplots(6, 5, figsize=(20, 18))

        axes = axes.flatten()

        for i, column in enumerate(data.columns):
            axes[i].hist(data[column], color='#8DBD85', bins=50)
            axes[i].set_title(f'{column}')
            axes[i].legend('Knight')

        plt.tight_layout()

        plt.savefig('Test_knight.png')
        plt.close()
    except FileNotFoundError as e:
        print(f"{e}")

def understand_interaction():
    try:
        data = pd.read_csv('../Train_knight.csv')

        fig, axes = plt.subplots(6, 5, figsize=(20, 18))

        axes = axes.flatten()

        for i, column in enumerate(data.columns):
            if column == 'knight':
                continue
            axes[i].hist(data[data['knight'] == 'Jedi'][column], alpha=0.3, color='blue', label='Jedi', bins=50)
            axes[i].hist(data[data['knight'] == 'Sith'][column], alpha=0.3, color='red', label='Sith', bins=50)

            axes[i].set_title(f'{column}')
            axes[i].legend()

        plt.tight_layout()

        plt.savefig('Train_knight.png')
        plt.close()
    except FileNotFoundError as e:
        print(f"{e}")

def main():
    visualize_knight_data()
    understand_interaction()

if __name__ == "__main__":
    main()