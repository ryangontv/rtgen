import json
import requests
import time
import re

programname = """
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▄▀█▄░▄█░▄▄▄█░▄▄█░▄▄▀██
█░▀▀▄██░██░█▄▀█░▄▄█░██░██
█▄█▄▄██▄██▄▄▄▄█▄▄▄█▄██▄██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
Generate radiotext data easy!
         v1.0.1
"""
print(programname)

last_title = ""
max_retries = 3  # Maximum number of retries for fetching JSON data.

# Enter icecast URL here
json_url = '<ICECAST-IP>/status-json.xsl?mount=/<mount>.mp3'
np_file_path = 'np.txt' # YOU NEED TO CREATE THESE FILES
song_file_path = 'song.txt' # YOU NEED TO CREATE THESE FILES
artist_file_path = 'artist.txt' # YOU NEED TO CREATE THESE FILES

retry_count = 0

while True:
    try:
        response = requests.get(json_url)
        
        if response.status_code == 200:
            data = response.json()
            
            icestats = data.get('icestats', {})
            source = icestats.get('source', {})
            title = source.get('title', '')

            if title != last_title:
                cleaned_title = re.sub(r'\([^)]*\)', '', title)

                if len(cleaned_title) > 64:
                    cleaned_title = cleaned_title[:61] + "..."

                with open(np_file_path, 'w') as np_file:
                    np_file.write(cleaned_title)

                match = re.match(r'(.+?) - (.+)', cleaned_title)
                if match:
                    artist, song = match.groups()
                else:
                    artist = song = cleaned_title

                with open(artist_file_path, 'w') as artist_file:
                    artist_file.write(artist.strip())  # Remove leading/trailing whitespaces

                with open(song_file_path, 'w') as song_file:
                    song_file.write(song.strip())  # Remove leading/trailing whitespaces

                last_title = title
                print(f"Title changed to: {title}")
                retry_count = 0  
        else:
            print(f"Failed to fetch JSON data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch JSON data: {str(e)}")
        retry_count += 1
        if retry_count > max_retries:
            print("Maximum retry limit reached. Exiting.")
            break
        time.sleep(60) 
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(10)  # Wait for 10 seconds before checking again, this can be changed.

