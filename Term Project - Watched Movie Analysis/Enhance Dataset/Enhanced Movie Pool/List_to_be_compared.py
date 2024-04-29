
import pandas as pd
import requests
import os
#import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Load your movie dataset into a DataFrame
file_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\list.csv'
random_df = pd.read_csv(file_path)


# Function to extract top 5 actors/actresses from the given Letterboxd URI
def extract_top_5_actors(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            cast_section = soup.find('div', {'id': 'tab-cast'})
            if cast_section:
                actor_links = cast_section.find_all('a', class_='text-slug tooltip')
                # Ensure only top 5 actors are included
                top_actors = [link.text for link in actor_links[:5]]
                # Pad the list with None if there are less than 5 actors
                top_actors += [None] * (5 - len(top_actors))
                return top_actors
            else:
                # If cast_section is not found, pad the list with None
                return [None] * 5
        else:
            # If response status is not 200, pad the list with None
            return [None] * 5
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        # If an exception occurs, pad the list with None
        return [None] * 5
    
# Function to extract director from the given Letterboxd URI
def extract_director(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            crew_section = soup.find('div', {'id': 'tab-crew'})
            if crew_section:
                director_link = crew_section.find('a', class_='text-slug')
                if director_link:
                    director_name = director_link.text
                    return director_name
                else:
                    return None
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None

def extract_language(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Switch to the 'tab-details' section
            details_section = soup.find('div', {'id': 'tab-details'})
            if details_section:
                # Find the language within the 'tab-details' section
                language_link = details_section.find('a', class_='text-slug', string='English')
                if language_link:
                    language_name = language_link.text
                    return language_name
                else:
                    return None
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None
    
def extract_genres(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Switch to the 'tab-genres' section
            genres_section = soup.find('div', {'id': 'tab-genres'})
            if genres_section:
                # Find all genre links within the 'tab-genres' section
                genre_links = genres_section.find_all('a', class_='text-slug')
                genres = [genre_link.text for genre_link in genre_links]
                return genres
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None

def extract_top_5_themes(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Switch to the 'tab-genres' section
            genres_section = soup.find('div', {'id': 'tab-genres'})
            if genres_section:
                # Find the 'Themes' section within the 'tab-genres' section
                themes_section = genres_section.find('h3', string='Themes') 
                if themes_section:
                    # Find all theme links within the 'Themes' section
                    theme_links = themes_section.find_next('div', class_='text-sluglist').find_all('a', class_='text-slug')
                    
                    # Extract only the top 5 themes or less
                    top_5_themes = [theme_link.text for theme_link in theme_links[:5]]
                    return top_5_themes
                else:
                    return None
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None



# Use ThreadPoolExecutor to parallelize the extraction of top actors
with ThreadPoolExecutor(max_workers=35) as executor:
    # Process the 'Letterboxd URI' column and add the 'Top Actors' column dynamically
    #movies_df['Rating'] = list(executor.map(extract_rating, movies_df['Letterboxd URI']))
    random_df['Top Actors'] = list(executor.map(extract_top_5_actors, random_df['Letterboxd URI']))
    random_df['Director'] = list(executor.map(extract_director, random_df['Letterboxd URI']))
    random_df['Genres'] = list(executor.map(extract_genres, random_df['Letterboxd URI']))
    random_df['Themes'] = list(executor.map(extract_top_5_themes, random_df['Letterboxd URI']))
    random_df['Language'] = list(executor.map(extract_language, random_df['Letterboxd URI']))
    #movies_df['Watched'] = list(executor.map(extract_watched_count, movies_df['Letterboxd URI']))
    #movies_df['Listed'] = list(executor.map(extract_listed_count, movies_df['Letterboxd URI']))
    #movies_df['Liked'] = list(executor.map(extract_liked_count, movies_df['Letterboxd URI']))



# Data cleaning part applied for only language section
mode_language = random_df['Language'].mode().iloc[0]  # Calculate mode
# Fill missing values in 'Language' column with the mode value
random_df['Language'].fillna(mode_language, inplace=True)


# Print the dataFrame to the console
print(random_df)

# Specify the path where you want to save the Excel file
excel_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\list_to_be_compared.xlsx'

# Ensure the directory exists, if not, create it
output_directory = os.path.dirname(excel_path)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Write the DataFrame to an Excel file
random_df.to_excel(excel_path, index=False)

print("Movies dataframe is fulfilled to the excel file")
