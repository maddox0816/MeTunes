"""
Spotify knockoff called MeTunes powered by flask.

downloads songs using youtube dl if they are not already downloaded
"""

import flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import youtube_dl
from youtube_search import YoutubeSearch
import os
import spotify

app = Flask(__name__)
app.static_url_path = '/static'


@app.route('/')
def index():
    songs=[]
    musics_file = open('songs list', 'r')
    musics_file_list =  musics_file.readlines()
    length = len(musics_file_list)
    print(length)
    for i in range(length):
        temp = musics_file_list[i].split('|:|')
        songs.append({'file': temp[0], 'title': temp[1], 'artist': temp[2], 'time': temp[3].replace('\n', ''), 'id': i+1, 'image': temp[4]})
       
    #order songs aphabeticly by title
    songs.sort(key=lambda x: x['title'].lower())
    print(songs)

    return render_template('index.html',songs=songs)


@app.route('/search', methods=['POST'])
def search():
    """
    Search for songs using youtube_dl

    get search_term post paramter
    """
    search_term = request.form.get('search_term') + " lyric video"

    print(search_term)
    ydl_opts = {
        'format': 'bestaudio/best',
    }
    
    #search for song on youtube
    results = YoutubeSearch(search_term, max_results=1).to_dict()
    print(results)
    url_to_download = "https://www.youtube.com" + results[0]['url_suffix']
    print(url_to_download)
    
    
    #download song
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #get files information
        result = ydl.extract_info(
        (url_to_download),
        download=False # We just want to extract the info
        )

        #file full name
        file_name = result['title'] + "-" + results[0]['id'] +  "." + result['ext']
        #check if file already exists
        if os.path.isfile("static/" + file_name):
            print("file already exists")
        else:
            #download song
            ydl.download([url_to_download])
            #move file to static folder
            os.rename(file_name, "static/" + file_name)
            #add file to list

            #get song details from spotify
            song_title, song_artist, album_image_url, release_date = spotify.get_song_details(results[0]['title'])

            file = open("songs list", "a")
            file.write(file_name + "|:|" + song_title + "|:|" + song_artist + "|:|" + release_date + "|:|" + album_image_url + "\n")

    return redirect(url_for('index'))
        






app.run(host='0.0.0.0', port=8080, debug=True)