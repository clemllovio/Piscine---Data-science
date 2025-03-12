import pandas as pd

def get_correlation_matrix(path):
    try:
        data = pd.read_csv(path)
        data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
        correlation = data.corr()["knight"].abs().sort_values(ascending=False)
        return correlation
    except FileNotFoundError:
        print(f'{e}')
        return None

def main():
    print(get_correlation_matrix("../Train_knight.csv"))

if __name__ == "__main__":
    main()