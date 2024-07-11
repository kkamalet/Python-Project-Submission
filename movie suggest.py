import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_movies(genre):
    try:
        url = f"https://www.imdb.com/search/title/?genres={genre}&sort=user_rating,desc&title_type=feature&num_votes=25000,"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        movies = []

        for movie in soup.find_all('div', class_='lister-item mode-advanced'):
            title = movie.h3.a.text
            rating = movie.find('div', class_='inline-block ratings-imdb-rating').strong.text
            movies.append({'Title': title, 'Rating': rating})
        
        if not movies:
            print("No movies found for the given genre.")
            return
        
        df = pd.DataFrame(movies)
        csv_file = f'{genre}_movies.csv'
        df.to_csv(csv_file, index=False)
        print(f"Data scraped and saved to {csv_file}")

        # Display the top 10 movies
        print("\nTop 10 Movies:")
        for idx, movie in enumerate(movies[:10], start=1):
            print(f"{idx}. {movie['Title']} - Rating: {movie['Rating']}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def display_movies_from_csv(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        print(f"\nMovies from {csv_file}:\n")
        print(df)
        print("\nTop 10 Movies:")
        for idx, row in df.iterrows():
            if idx >= 10:
                break
            print(f"{idx+1}. {row['Title']} - Rating: {row['Rating']}")
    else:
        print(f"{csv_file} does not exist. Please ensure the file is in the correct directory.")

if __name__ == "__main__":
    choice = input("Do you want to (1) scrape movies or (2) read from 'movies.csv'? Enter 1 or 2: ").strip()
    
    if choice == '1':
        genre = input("Enter the movie genre: ").strip().lower()
        scrape_movies(genre)
    
    else:
        print("Invalid choice. Please enter 1 to scrape movies or 2 to read from 'movies.csv'.")



