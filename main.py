from time import sleep
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

username = input("MAL Username: ")

# Make request to Mal
req = requests.get(f"https://myanimelist.net/animelist/{username}/load.json")
shows = req.json()

# Check if there are any errors, usually caused by an invalid request
if(isinstance(shows, dict) and shows['errors']):
    print(f"Error: {' '.join(map(lambda x: x['message'], shows['errors']))}")
    exit()

# Check if no shows on mal
if len(shows) == 0:
    print("Error: No shows found")
    quit()
else:
    print(f"{username} has {len(shows)} shows")

# Check if we should account for only completed shows (status 2)
completed_only = None
while completed_only == None:
    ans = input("Only analyse completed anime? [Yy/Nn]: ")
    if ans.lower() == "y":
        completed_only = True
    elif ans.lower() == "n":
        completed_only = False
    else:
        print("Invalid input")
        completed_only = None

# Filter if specified
if(completed_only):
    shows = list(filter(lambda x: x['status'] == 2, shows))

print(f"Attempting to analyse {len(shows)} shows")

total_score = 0
total_shows = len(shows)
with tqdm(shows) as t:
    for show in t:
        score = None
        t.set_description_str(f"{show['anime_title']}")
        while score == None:
            req = requests.get(f"https://myanimelist.net{show['anime_url']}")
            if (req.status_code == 200):
                soup = BeautifulSoup(req.text, "html.parser")
                score = soup.find("div", {"class": "score-label"}).text
                # Try-Except in case the score is missing, if so remove one show from total_shows
                try:
                    score = float(score)
                except:
                    score = 0
                    total_shows -= 1
            else:
                sleep(0.25)
        total_score += score

print(f"Total shows checked: {total_shows}, Total shows attempted to check: {len(shows)}")
print(f"Total score: {total_score}, Mean score: {total_score/total_shows}")