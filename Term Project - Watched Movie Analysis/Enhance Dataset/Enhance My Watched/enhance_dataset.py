import pandas as pd
import requests
import os
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Load your movie dataset into a DataFrame
file_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\watched.csv'
movies_df = pd.read_csv(file_path)

# Convert 'Date' column to datetime format
movies_df['Date'] = pd.to_datetime(movies_df['Date'], format='%Y-%m-%d', errors='coerce')


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

# Function to extract language from the given Letterboxd URI
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
    
# Function to extract language from the given Letterboxd URI    
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

# Function to extract top 5 themes from the given Letterboxd URI
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
    

# Function to extract numeric values from string from the given Letterboxd URI
def extract_numeric_value_from_string(value_string):
    try:
        # Use regular expression to extract numeric part
        numeric_value = re.search(r'\d+', value_string).group()
        return int(numeric_value)
    except Exception as e:
        print(f"Error extracting numeric value: {e}")
        return None

# Function to extract overall watched count from the given Letterboxd URI
def extract_watched_count(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            watched_count_section = soup.find('li', class_='filmstat-watches')
            if watched_count_section:
                watched_count_text = watched_count_section.get_text(strip=True)
                watched_count_value = extract_numeric_value_from_string(watched_count_text)
                return watched_count_value
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None
    
# Function to extract overall listed count from the given Letterboxd URI
def extract_listed_count(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            listed_count_section = soup.find('li', class_='filmstat-lists')
            if listed_count_section:
                listed_count_text = listed_count_section.get_text(strip=True)
                listed_count_value = extract_numeric_value_from_string(listed_count_text)
                return listed_count_value
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None

# Function to extract overall liked count from the given Letterboxd URI
def extract_liked_count(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            liked_count_section = soup.find('li', class_='filmstat-likes')
            if liked_count_section:
                liked_count_text = liked_count_section.find('a', class_='has-icon icon-like icon-liked icon-16 tooltip').get_text(strip=True)
                liked_count_value = extract_numeric_value_from_string(liked_count_text)
                return liked_count_value
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching {letterboxd_uri}: {e}")
        return None

# Function to extract rating from the given Letterboxd URI
def extract_rating(letterboxd_uri):
    try:
        response = requests.get(letterboxd_uri)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the rating section
            rating_section = soup.find('section', class_='ratings-histogram-chart')
            if rating_section:
                #Find the average rating value
                average_rating = rating_section.find('span', class_='average-rating').find('a', class_='tooltip').text.strip()
                # Extract other rating details if needed
                # For example, you can extract the number of fans
                fans_link = rating_section.find('a', class_='all-link more-link')
                fans_count = fans_link.text.strip() if fans_link else None
                return average_rating, fans_count
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error extracting rating info: {e}")
        return None, None


# Use ThreadPoolExecutor to parallelize the extraction of top actors
with ThreadPoolExecutor(max_workers=35) as executor:
    # Process the 'Letterboxd URI' column and add the 'Top Actors' column dynamically
    movies_df['Rating'] = list(executor.map(extract_rating, movies_df['Letterboxd URI']))
    movies_df['Top Actors'] = list(executor.map(extract_top_5_actors, movies_df['Letterboxd URI']))
    movies_df['Director'] = list(executor.map(extract_director, movies_df['Letterboxd URI']))
    movies_df['Genres'] = list(executor.map(extract_genres, movies_df['Letterboxd URI']))
    movies_df['Themes'] = list(executor.map(extract_top_5_themes, movies_df['Letterboxd URI']))
    movies_df['Language'] = list(executor.map(extract_language, movies_df['Letterboxd URI']))


# Data cleaning part applied for only language section
mode_language = movies_df['Language'].mode().iloc[0]  # Calculate mode
# Fill missing values in 'Language' column with the mode value
movies_df['Language'].fillna(mode_language, inplace=True)


# Print the dataFrame to the console
print(movies_df)

# Specify the path where you want to save the Excel file
excel_path = r'C:\Users\İpek Akkuş\Source\Repos\termProject\extracted1.xlsx'

# Ensure the directory exists, if not, create it
output_directory = os.path.dirname(excel_path)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Write the DataFrame to an Excel file
movies_df.to_excel(excel_path, index=False)

print("Movies dataframe is fulfilled to the excel file")
