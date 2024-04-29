# EDA Document

import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns


# Specify the path where the Excel file is located
excel_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\extracted1.xlsx'

# Read the Excel file into a new DataFrame
movies_df = pd.read_excel(excel_path)


'''
Let's explore our data frame
Some descriptive stats are placed below. 
'''

# Display the first few rows of the DataFrame
print("First few rows of the DataFrame:")
print(movies_df.head(10))

# Display general information about the DataFrame
print("\nInfo:")
print(movies_df.info())

# Display descriptive statistics for numeric columns
print("\nDescriptive Statistics:")
print(movies_df.describe(include='all'))

# Display the number of non-null observations in each column
print("\nCount of non-null observations:")
print(movies_df.count())

# Checked the data types of each column using dtypes.
print("Data types")
data_types = movies_df.dtypes
print(data_types)

# Identified missing values using isnull() or info().
print("Missing Values")
missing_values = movies_df.isnull().sum()
print(missing_values)


'''
Top Actors and Directors:

Identify the most frequent actors and directors in your dataset. 
This will help you understand who the dominant figures are in the movies 
I've watched.
Visualize the top actors and directors using bar plots or word clouds.

'''
'''
Display 20 most occurred actors
'''
# Convert string representation of lists to actual lists
movies_df['Top Actors'] = movies_df['Top Actors'].apply(ast.literal_eval)

# Create a new DataFrame with each actor in a separate row
actors_df = movies_df.explode('Top Actors')

# Count the occurrences of each actor
actor_counts = actors_df['Top Actors'].value_counts()

# Reset the index to create a DataFrame
actors_df = actor_counts.reset_index()

# Rename the columns for clarity
actors_df.columns = ['Actor', 'Movie Count']

# Display the resulting DataFrame
print("Data frame of actors")
print(actors_df)

# Get the top 10 actors
top_10_actors = actors_df.head(10)

# Plotting the histogram
plt.figure(figsize=(12, 6))
plt.bar(top_10_actors['Actor'], top_10_actors['Movie Count'], color='skyblue')
plt.xlabel('Actor')
plt.ylabel('Movie Count')
plt.title('Top 10 Actors and Their Movie Counts')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the histogram
plt.show()


'''
Display 15 most occurred directors
'''
# Initialize an empty dictionary to store director counts
director_counts = {}

# Iterate over the 'Director' column
for director in movies_df['Director']:
    # Increment the count for each director
    director_counts[director] = director_counts.get(director, 0) + 1

# Sort the director counts in descending order
sorted_director_counts = sorted(director_counts.items(), key=lambda x: x[1], reverse=True)

# Print the top 15 directors
print("Top 15 Directors:")
for i, (director, count) in enumerate(sorted_director_counts[:15], start=1):
    print(f"{i}. {director}: {count} movies")

# Display these top directors in a histogram
# Extract top 15 directors and their counts
top_15_directors = [director[0] for director in sorted_director_counts[:15]]
top_15_director_counts = [director[1] for director in sorted_director_counts[:15]]

# Plotting the histogram
plt.figure(figsize=(12, 6))
plt.bar(top_15_directors, top_15_director_counts, color='lightcoral')
plt.xlabel('Director')
plt.ylabel('Count')
plt.title('Top 15 Directors and Their Occurrence Counts')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the histogram
plt.show()

'''
Genres and Themes:

Explore the distribution of movie genres and themes in your dataset.
This will help us understand your preferences and the diversity of 
genres/themes in watched movies.
Visualize the distribution using bar plots.

'''

'''
Display 10 most occurred genres
'''
# Convert string representation of lists to actual lists
movies_df['Genres'] = movies_df['Genres'].apply(ast.literal_eval)

# Create a new DataFrame with each genre in a separate row
genres_df = movies_df.explode('Genres')

# Filter out 'Show All' genre
genres_df = genres_df[genres_df['Genres'] != 'Show All']

# Count the occurrences of each genre
genre_counts = genres_df['Genres'].value_counts()

# Reset the index to create a DataFrame
genres_df = genre_counts.reset_index()

# Rename the columns for clarity
genres_df.columns = ['Genre', 'Movie Count']

# Select genres from index 1 to 11
selected_genres = genres_df.iloc[1:11]

print("Top genres")
print(selected_genres)

# Plotting the histogram with counts labeled on top of each bar
plt.figure(figsize=(12, 6))
bars = plt.bar(selected_genres['Genre'], selected_genres['Movie Count'], color='lightgreen')

# Add labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

plt.xlabel('Genre')
plt.ylabel('Movie Count')
plt.title('Genres and Their Movie Counts (Index 1 to 11)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the histogram
plt.show()


'''
Display 10 most occurred themes
'''
def safe_eval(value):
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return None

# Convert string representation of lists to actual lists using the safe_eval function
movies_df['Themes'] = movies_df['Themes'].apply(safe_eval)

# Create a new DataFrame with each theme in a separate row
themes_df = movies_df.explode('Themes')

# Drop rows with missing values in the 'Themes' column
themes_df = themes_df.dropna(subset=['Themes'])

# Count the occurrences of each theme
theme_counts = themes_df['Themes'].value_counts()

# Reset the index to create a DataFrame
themes_df = theme_counts.reset_index()

# Rename the columns for clarity
themes_df.columns = ['Theme', 'Movie Count']

# Get the top 10 themes
top_10_themes = themes_df.head(10)

# Plotting the histogram with counts labeled on top of each bar
plt.figure(figsize=(12, 6))
bars = plt.bar(top_10_themes['Theme'], top_10_themes['Movie Count'], color='orange')

# Add labels on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

plt.xlabel('Theme')
plt.ylabel('Movie Count')
plt.title('Top 10 Themes and Their Movie Counts')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Display the histogram
plt.show()




'''
How much I am following the trends over the years?

2010 decided according to the year that I was born. Note that I was born in 2003. 
Movies elder than me starting to understand movies creates biases.
'''
'''
Interpretation
If the bars are generally positive, it means that, on average, you are watching movies a certain number of years after their release.
If the error bars are small, it indicates less variability in the time differences for movies released in that year.
If the error bars are large, it suggests more variability in the time differences.
For example, if you see a positive bar for a specific year with small error bars, 
'''

# Assuming 'Date' column is in the format 'YYYY-MM-DD'
movies_df['Date'] = pd.to_datetime(movies_df['Date'], errors='coerce')

# Filter movies released after 2010
filtered_movies_df = movies_df[movies_df['Year'] > 2015]

# Calculate the time difference
filtered_movies_df['Time Difference'] = filtered_movies_df['Date'].dt.year - filtered_movies_df['Year']

# Create a bar plot with error bars
plt.figure(figsize=(12, 6))

# Use seaborn barplot
ax = sns.barplot(x='Year', y='Time Difference', data=filtered_movies_df, ci='sd')

# Customize error bars with labels
for i, bar in enumerate(ax.patches):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    sd = filtered_movies_df.groupby('Year')['Time Difference'].std().iloc[i]
    
    ax.errorbar(x, y, yerr=sd, fmt=' ', color='black', capsize=5, label=f'{sd:.2f}')
    ax.text(x, y + sd + 0.2, f'{sd:.2f}', ha='center', va='bottom', color='black', fontsize=8)
    
# Add labels and title
plt.title('Time Difference Between Release Year and Watched Year Over Time')
plt.xlabel('Release Year')
plt.ylabel('Time Difference')

# Show the plot
plt.show()




