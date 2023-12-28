# Source code by https://isabella-b.com/blog/scraping-episode-imdb-ratings-tutorial/

# Install requests via the cmd line first: pip3 install requests
# Install bs4 (beautiful soup 4) via the cmd line first: pip3 install bs4
# Instal pandas via the cmd line first: pip3 install pandas

from requests import get
from bs4 import BeautifulSoup
import pandas as pd

# Initializing the series that the loop will populate
bob_ross_episodes = []

# For every season in the series-- range depends on the show - make sure to add 1
# to the end
for sn in range(1, 32):
    # Request from the server the content of the web page by using get(), and store the server’s response in the variable response
    response = get('https://www.imdb.com/title/tt0383795/episodes?season=' + str(sn))

    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')

    # Select all the episode containers from the season's page
    episode_containers = page_html.find_all('div', class_ = 'info')

    # For each episode in each season
    for episodes in episode_containers:
            # Get the info of each episode on the page
            season = sn
            episode_number = episodes.meta['content']
            title = episodes.a['title']
            airdate = episodes.find('div', class_='airdate').text.strip()
            rating = episodes.find('span', class_='ipl-rating-star__rating').text
            # If there is an error then do a try/except clause like below
            try:
                total_votes = episodes.find('span', class_='ipl-rating-star__total-votes').text
            except:
                pass
            desc = episodes.find('div', class_='item_description').text.strip()
            # Compiling the episode info
            episode_data = [season, episode_number, title, airdate, rating, total_votes, desc]
            # Append the episode info to the complete dataset
            bob_ross_episodes.append(episode_data)

bob_ross_episodes = pd.DataFrame(bob_ross_episodes, columns = ['season', 'episode_number', 'title', 'airdate', 'rating', 'total_votes', 'desc'])

bob_ross_episodes.to_csv('Bob_Ross_IMDb_Ratings.csv',index=False)
