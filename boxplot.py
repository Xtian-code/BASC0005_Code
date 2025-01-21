import pandas as pd
import matplotlib.pyplot as plt

# Define the file path
file_path = 'reviewscore.xlsx'

# Load file
data = pd.ExcelFile(file_path)

# Parse the first sheet into a DataFrame
df = data.parse('Sheet1')

# Reshape the data from wide format to long format for easier visualisation
df_long = df.melt(
    var_name="genre",                
    value_name="reviewscore",        
    value_vars=["Independent", "Casual", "Action"]  
)

# Drop rows with missing values to ensure data clean
df_long = df_long.dropna()

# Create the boxplot
plt.figure(figsize=(8, 6))  
df_long.boxplot(column="reviewscore", by="genre", grid=False)  

# Add titles and labels
plt.title("Review Score Comparison by Genre")  
plt.suptitle("")  
plt.xlabel("Genre")  
plt.ylabel("Review Score")  

# Display the plot
plt.show()
