# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Define the file path for the Excel file
file_path = 'reviewscore.xlsx'

# Load the Excel file
data = pd.ExcelFile(file_path)

# Parse the first sheet into a DataFrame
df = data.parse('Sheet1')

# Reshape the data from wide format to long format for easier visualization
df_long = df.melt(
    var_name="genre",                # Column to store variable names
    value_name="reviewscore",        # Column to store values
    value_vars=["Independent", "Casual", "Action"]  # Columns to unpivot
)

# Drop rows with missing values to ensure clean data
df_long = df_long.dropna()

# Create the boxplot
plt.figure(figsize=(8, 6))  # Set figure size
df_long.boxplot(column="reviewscore", by="genre", grid=False)  # Generate boxplot

# Add titles and labels
plt.title("Review Score Comparison by Genre")  # Title of the plot
plt.suptitle("")  # Remove the default Matplotlib subtitle
plt.xlabel("Genre")  # Label for the x-axis
plt.ylabel("Review Score")  # Label for the y-axis

# Display the plot
plt.show()
