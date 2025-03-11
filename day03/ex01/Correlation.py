import pandas as pd

def get_correlation_matrix(path):
    data = pd.read_csv(path)
    data['knight'] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    numeric_data = data.select_dtypes(include=['number']).dropna()
    correlation = numeric_data.corr()["knight"].abs().sort_values(ascending=False)
    return correlation

def main():
    print(get_correlation_matrix("../Train_knight.csv"))

if __name__ == "__main__":
    main()