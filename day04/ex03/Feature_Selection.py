import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler

def standarized_data(data):
    scaler = StandardScaler()
    numeric_data = data.select_dtypes(include=['number'])
    standardized_data = scaler.fit_transform(numeric_data)
    standardized_df = pd.DataFrame(standardized_data, columns=numeric_data.columns)
    standardized_df["knight"] = data['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    return standardized_df

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

    standarized_df = standarized_df.drop(columns=["knight"])

    vif_data = pd.DataFrame()
    vif_data["Feature"] = standarized_df.columns
    vif_data["VIF"] = [variance_inflation_factor(standarized_df.values, i)
                          for i in range(len(standarized_df.columns))]
    vif_data["Tolerance"] = [1 / vif for vif in vif_data["VIF"]]
    print(vif_data)

    print("\n\n")

    feature_under_5 = vif_data[vif_data["VIF"] < 5]
    print("Feature with vif < 5:\n", feature_under_5)

if __name__ == '__main__':
    main()