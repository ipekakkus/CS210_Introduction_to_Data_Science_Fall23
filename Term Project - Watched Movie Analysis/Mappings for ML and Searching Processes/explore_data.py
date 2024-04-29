import pandas as pd
import ast

def safe_eval(value):
    try:
        return ast.literal_eval(value) if value is not None else []
    except (SyntaxError, ValueError):
        return []

my_file_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\extracted1.xlsx'
dataset = pd.read_excel(my_file_path)

search_file_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\list_to_be_compared.xlsx'
dataset1 = pd.read_excel(search_file_path)

# Assuming you have columns 'Genres', 'Top Actors', 'Director', 'Themes' in your dataset
# Convert string representation of lists to actual lists
dataset['Top Actors'] = dataset['Top Actors'].apply(lambda x: x if isinstance(x, list) else ast.literal_eval(x))
actors_df = dataset.explode('Top Actors')
actor_counts = actors_df['Top Actors'].value_counts()
actors_df = actor_counts.reset_index()
actors_df.columns = ['Actor', 'Movie Count']
top_actors = actors_df.head(10)

director_counts = {}
for director in dataset['Director']:
    # Increment the count for each director
    director_counts[director] = director_counts.get(director, 0) + 1
sorted_director_counts = sorted(director_counts.items(), key=lambda x: x[1], reverse=True)
print("Top 15 Directors:")
for i, (director, count) in enumerate(sorted_director_counts[:15], start=1):
    print(f"{i}. {director}: {count} movies")

top_directors = [director[0] for director in sorted_director_counts[:15]]
top_director_counts = [director[1] for director in sorted_director_counts[:15]]
data = {'Director': top_directors, 'Movie_Count': top_director_counts}
top_directors_df = pd.DataFrame(data).head(15)

dataset['Genres'] = dataset['Genres'].apply(lambda x: x if isinstance(x, list) else ast.literal_eval(x))
genres_df = dataset.explode('Genres')
genres_df = genres_df[genres_df['Genres'] != 'Show All']
genre_counts = genres_df['Genres'].value_counts()
genres_df = genre_counts.reset_index()
genres_df.columns = ['Genre', 'Movie Count']
top_genres = genres_df.iloc[1:11]

# Handling 'Themes' mapping for each theme individually
dataset['Themes'] = dataset['Themes'].apply(safe_eval)
themes_df = dataset.explode('Themes')
themes_df = themes_df.dropna(subset=['Themes'])
theme_counts = themes_df['Themes'].value_counts()
themes_df = theme_counts.reset_index()
themes_df.columns = ['Theme', 'Movie Count']
top_themes = themes_df.head(10)

dataset['Top Actors'] = dataset['Top Actors'].apply(lambda x: x if isinstance(x, list) else ast.literal_eval(x))
dataset['Themes'] = dataset['Themes'].apply(safe_eval)

# Manually create a mapping for each column based on top values calculated above
actor_mapping = {'Christian Bale': 10,'Brad Pitt':9,'Keanu Reeves': 8,
                 'Scarlett Johansson': 7,'Joaquin Phoenix': 6,'Laurence Fishburne': 5,
                 'Al Pacino': 4,'Leonardo DiCaprio':3,'Ryan Gosling': 2,
                 'Willem Dafoe': 1}

director_mapping = {'Christopher Nolan': 15,'Terrence Malick':14,'Dennis Villeneuve': 13,
                 'Andrei Tarkovsky':12,'Quentin Tarantino': 11,'Paul Thomas Anderson': 10,
                 'Lars von Trier': 9,'David Fincher':8,'Peter Jackson': 7,
                 'Michael Haneke':6, 'Krzysztof Kieślowski ': 5,
                 'Joel Coen': 4,'Martin Scorsese':3,'Darren Aronofsky': 2,
                 'Ridley Scott':1 }

genre_mapping = {'Drama': 10,'Moving relationship stories':9,'Thriller': 8,
                 'Humanity and the world around us': 7,'Intense violence and sexual transgression': 6,'Surreal and thought-provoking visions of life and death': 5,
                 'Mystery': 4,'Romance':3,'Faith and religion': 2,
                 'Epic history and literature': 1}
theme_mapping = {'Moving relationship stories': 10,'Humanity and the world around us':9,'Intense violence and sexual transgression': 8,
                 'Faith and religion': 7,'Epic history and literature': 6,'Thrillers and murder mysteries': 5,
                 'Surreal and thought-provoking visions of life and death': 4,'Monsters, aliens, sci-fi and the apocalypse':3,'Horror, the undead and monster classics': 2,
                 'Gothic and eerie haunting horror': 1}

# Apply mappings to the dataset
dataset['Encoded_Actor'] = dataset['Top Actors'].apply(lambda x: [actor_mapping.get(actor, 0) for actor in x])
dataset['Encoded_Director'] = dataset['Director'].map(director_mapping)

# Handling 'Genres' mapping for each genre individually
genres_df['Encoded_Genre'] = genres_df['Genres'].map(genre_mapping)
genre_score = genres_df.groupby(genres_df.index)['Encoded_Genre'].sum()
dataset['Encoded_Genre'] = dataset.index.map(genre_score).fillna(0)

# Handling 'Themes' mapping for each theme individually
themes_df['Encoded_Theme'] = themes_df['Themes'].map(theme_mapping)
theme_score = themes_df.groupby(themes_df.index)['Encoded_Theme'].sum()
dataset['Encoded_Theme'] = dataset.index.map(theme_score).fillna(0)

# Assuming 'searched_movie' is the DataFrame with the information of the user-entered movie
searched_movie = dataset1.head(1)

# Function to calculate similarity score
def calculate_similarity(movie, actor_mapping, director_mapping, genre_mapping, theme_mapping):
    actor_score = sum(actor_mapping.get(actor, 0) for actor in movie['Top Actors'])
    director_score = director_mapping.get(movie['Director'], 0)
    genre_score = movie['Encoded_Genre']
    theme_score = movie['Encoded_Theme']
    total_score = actor_score + director_score + genre_score + theme_score
    return total_score

# Calculate similarity scores for each watched movie
dataset['Similarity Score'] = dataset.apply(
    lambda row: calculate_similarity(row, actor_mapping, director_mapping, genre_mapping, theme_mapping),
    axis=1
)

# Sort the dataset based on similarity scores
sorted_movies = dataset.sort_values(by='Similarity Score', ascending=False)

# Display the top similar movies
top_similar_movies = sorted_movies[['Title', 'Similarity Score']].head(10)
print("Top Similar Movies:")
print(top_similar_movies)
