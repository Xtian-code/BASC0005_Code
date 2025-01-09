import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Load Data
file_path = 'All_games_vf.xlsx'
df = pd.ExcelFile(file_path).parse('DB')

# 2. Data Cleaning
columns_to_keep = ['Genre', 'reviewScore', 'revenue', 'copiesSold', 'price', 'firstReleaseDate']
df_cleaned = df[columns_to_keep].dropna()

# Apply log transformation to 'revenue' and 'copiesSold'
df_cleaned['log_revenue'] = np.log(df_cleaned['revenue'] + 1)  # Avoid log(0)
df_cleaned['log_copiesSold'] = np.log(df_cleaned['copiesSold'] + 1)

# 3. Regression Analysis Function
def perform_regression(df, dependent_var, independent_var):
    results = {}
    grouped = df.groupby('Genre')
    for genre, group in grouped:
        # Define variables
        X = group[independent_var]
        y = group[dependent_var]

        # Add constant for OLS regression
        X = sm.add_constant(X)

        # Fit the model
        model = sm.OLS(y, X).fit()

        # Store OLS summary including R-squared in output
        summary = model.summary()
        summary.tables[0].data.append(["R-squared", "", "", "", f"{model.rsquared:.4f}"])

        results[genre] = summary
    return results

# 4. Visualisation Function with Pearson Correlation
def plot_scatter_with_regression(df, x_var, y_var):
    genres = df['Genre'].unique()
    for genre in genres:
        subset = df[df['Genre'] == genre]

        if y_var not in subset or subset[y_var].isna().all():
            print(f"Skipping {genre} due to lack of data for {y_var}.")
            continue

        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=subset, x=x_var, y=y_var, alpha=0.5)

        # Add regression line
        sns.regplot(data=subset, x=x_var, y=y_var, scatter=False, color='red')

        # Compute Pearson correlation
        corr = subset[x_var].corr(subset[y_var])

        # Title with correlation and genre
        plt.title(f'{genre} Games: {x_var} vs {y_var}\nCorrelation: {corr:.2f}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.show()

# 5. Perform Regression for Revenue and Copies Sold
revenue_results = perform_regression(df_cleaned, 'log_revenue', 'reviewScore')
copies_sold_results = perform_regression(df_cleaned, 'log_copiesSold', 'reviewScore')

# 6. Visualise Revenue vs Review Score
print("\n--- Revenue Regression Results ---\n")
for genre, summary in revenue_results.items():
    print(f"{genre} Games:\n{summary}")

plot_scatter_with_regression(df_cleaned, 'reviewScore', 'log_revenue')

# 7. Visualise Copies Sold vs Review Score
print("\n--- Copies Sold Regression Results ---\n")
for genre, summary in copies_sold_results.items():
    print(f"{genre} Games:\n{summary}")

plot_scatter_with_regression(df_cleaned, 'reviewScore', 'log_copiesSold')
