import requests

def get_song_details(search_term):
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": search_term,
        "type": "track",
        "limit": 1
    }
    OAuthToken = "BQCT9qIBeDFW5XgEHjohgP-unR8ac9xUL2ccll4ni_9I50_dxU0mSZ1czEcC-wXG7_9mX0EZV73qI89eyNEr-Z0VgxKL1R6srkwVNiJv8bbcfBWtS3YmDExWf8o-nhJj8UdPSs4x8r-P2nJJs1jt-dq1hMVo-SOfo4c"

    headers = {
        "Authorization": "Bearer " + OAuthToken
    }
    response = requests.get(url, params=params, headers=headers)
    print(response.json())

    song_title = response.json()['tracks']['items'][0]['name']


    song_artist = response.json()['tracks']['items'][0]['artists'][0]['name']


    album_image_url = response.json()['tracks']['items'][0]['album']['images'][0]['url']

    try:
        release_date = response.json()['tracks']['items'][0]['album']['release_date']
        release_date = release_date.split('-')
        release_date = release_date[1] + '/' + release_date[2] + '/' + release_date[0]
    except:
        release_date = "N/A"


    print(song_title)
    print(song_artist)
    print(album_image_url)
    print(release_date)

    return song_title, song_artist, album_image_url, release_date


#get_song_details("You Spin Me Round (Liek a recod)")