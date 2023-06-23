import requests
import sqlite3

# API endpoint URL
url = "https://premier-league-standings1.p.rapidapi.com/"

# Headers with RapidAPI key and host
headers = {
    "X-RapidAPI-Key": "d5c307c9d2msh171b0eb139794dcp123df6jsnb413743e6dfe",
    "X-RapidAPI-Host": "premier-league-standings1.p.rapidapi.com"
}

# Make a GET request to the API
response = requests.get(url, headers=headers)
print(response.json())

# Check if the response was successful (status code 200)
if response.status_code == 200:
    premier_league_data = response.json()

    # Create a connection to the SQLite database
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()

    # Delete the "teams" and "stats" table if they exist
    cursor.execute("DROP TABLE IF EXISTS teams")
    cursor.execute("DROP TABLE IF EXISTS stats")

    # Create the "teams" table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            logo TEXT NOT NULL,
            abbreviation TEXT NOT NULL
        )
    ''')
    team_data = []
    for item in premier_league_data:
        team = item['team']
        name = team['name']
        logo = team['logo']
        abbreviation = team['abbreviation']
        team_data.append((name, logo, abbreviation))

    # Insert team data into the "teams" table
    cursor.executemany('INSERT INTO teams (name, logo, abbreviation) VALUES (?, ?, ?)', team_data)

    # Create the "stats" table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wins INTEGER NOT NULL,
            losses INTEGER NOT NULL,
            ties INTEGER NOT NULL,
            gamesPlayed INTEGER NOT NULL,
            goalsFor INTEGER NOT NULL,
            goalsAgainst INTEGER NOT NULL,
            points INTEGER NOT NULL,
            rank INTEGER NOT NULL,
            goalDifference INTEGER NOT NULL
        )
    ''')
    team_stats = []
    for item in premier_league_data:
        stats = item['stats']
        wins = stats['wins']
        losses = stats['losses']
        ties = stats['ties']
        gamesPlayed = stats['gamesPlayed']
        goalsFor = stats['goalsFor']
        goalsAgainst = stats['goalsAgainst']
        points = stats['points']
        rank = stats['rank']
        goalDifference = stats['goalDifference']
        team_stats.append((wins, losses, ties, gamesPlayed, goalsFor, goalsAgainst, points, rank, goalDifference))

    # Insert team statistics into the "stats" table
    cursor.executemany('INSERT INTO stats (wins, losses, ties, gamesPlayed, goalsFor, goalsAgainst, points, rank, '
                       'goalDifference) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', team_stats)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
else:
    print('Error retrieving fixture data. Status code:', response.status_code)
