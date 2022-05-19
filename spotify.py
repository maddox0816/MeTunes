import requests

def get_song_details(search_term):
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": search_term,
        "type": "track",
        "limit": 1
    }
    OAuthToken = "BQDDOgiX-C51i3lylS-XkO9TjHLXbggFxrUeX8HqP86twRvQI1iCAD4-UOYN31BwqPEiGQETjmXNmw1Ih7HUmNMYhlpDPOd1grGGRQCGqxVi0_cRdRHoEQd2hmOvqLB27Nf2I6FiwMxP46PREK52JycAYOjYR2A1pbA"

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