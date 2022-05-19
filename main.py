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
import requests

app = Flask(__name__)
app.static_url_path = '/static'

download_stats={}

@app.route('/')
def index():
    songs=[]
    musics_file = open('songs list', 'r')
    musics_file_list =  musics_file.readlines()
    length = len(musics_file_list)
    print(length)
    for i in range(length):
        temp = musics_file_list[i].split('|:|')
        songs.append({'file': temp[0], 'title': temp[1], 'artist': temp[2], 'time': temp[3].replace('\n', ''), 'id': i+1, 'image': "/api/image-proxy?image_url=" + temp[4]})
       
    #order songs aphabeticly by title
    songs.sort(key=lambda x: x['title'].lower())
    print(songs)

    return render_template('index.html',songs=songs)



@app.route('/api/download-song', methods=['POST', 'GET'])
def DownloadSong():
    """
    Download song from youtube using youtube_dl and get information about the song from spotify
    """

    if request.method == 'POST':
        video_id = request.form.get('songid') 
    else:
        video_id = request.args.get('songid')

    print(video_id)
    
    
    #get best audio and rename the file to just its id and add callback to status-update function with the percent
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'progress_hooks': [status_update],

    }
    

    url_to_download = "https://www.youtube.com/watch?v=" + video_id
    print(url_to_download)
    
    
    #download song
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #get files information
        result = ydl.extract_info(
        (url_to_download),
        download=False # We just want to extract the info
        )

        #file full name
        file_name = video_id +  "." + result['ext']
        #check if file already exists
        if os.path.isfile("static/" + file_name):
            print("file already exists")
        else:
            #add song to status dictionary

            #download song 
            ydl.download([url_to_download])

            
            #add file to list

            #get song details from spotify
            song_title, song_artist, album_image_url, release_date = spotify.get_song_details(result["title"])

            file = open("songs list", "a")
            file.write(file_name + "|:|" + song_title + "|:|" + song_artist + "|:|" + release_date + "|:|" + album_image_url + "\n")
            file.close()

            #move file to static folder
            os.rename(file_name, "static/" + file_name)

    return redirect(url_for('index'))


@app.route('/api/search', methods=['POST','GET'])
def search():
    """
    Search for songs using youtube_dl

    get search_term post paramter
    """
    search_term = request.form.get('search_term') + " lyric video"

    print(search_term)
    
    
    #get best audio and rename the file to just its id and add callback to status-update function with the percent
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'progress_hooks': [status_update],

    }
    
    #search for song on youtube
    results = YoutubeSearch(search_term, max_results=1).to_dict()
    print(results)
    video_id = results[0]['id']
    print(video_id)
    
    return video_id 
        

    
        




    



def status_update(d):
    """
    Update download status
    """
    video_id = d['filename'].split('.')[0]

    if d['status'] == 'downloading':
        download_stats[video_id] = d['_percent_str']
        download_stats[video_id + '_ETA'] = d['_eta_str']
    elif d['status'] == 'finished':
        download_stats[video_id] = '100%'
    else:
        download_stats[video_id] = '0%'

        


@app.route('/api/download-status', methods=['POST', 'GET'])
def download_status():
    """
    Get download status
    """
    if request.method == 'POST':
        video_id = request.form.get('songid')
    else:
        video_id = request.args.get('songid')
    print(video_id)
    print(download_stats)
    try:
        if download_stats[video_id] != '100%' and download_stats[video_id] != '0%':
            thing_to_return = """
            <h5>Downloading...</h5>
            <h5>{}</h5>
            <div class="progress">
            <div class="progress-bar progress-bar-animated" role="progressbar" aria-valuenow="{}" aria-valuemin="0" aria-valuemax="100" style="width: {}">
            </div></div>
            """.format( "ETA: " + download_stats[video_id + '_ETA'], download_stats[video_id], download_stats[video_id])
        elif download_stats[video_id] == '100%':
            thing_to_return = """
            <h5>Downloaded!</h5>
            <div class="progress">
            <div class="progress-bar  progress-bar-animated" role="progressbar" aria-valuenow="{}" aria-valuemin="0" aria-valuemax="100" style="width: {}">
            </div></div><br>
            <button type="button" class="btn btn-primary" onclick="window.location.href='/'">Click to reload</button>
            """
        else:
            thing_to_return = """
            <h5>Download failed</h5>
            <button type="button" class="btn btn-primary" onclick="window.location.href='/'">Click to reload</button>
            """
        return thing_to_return
    except:
        yep = "it failed"


@app.route('/api/image-proxy', methods=['GET'])
def image_proxy():
    """
    Proxy for spotify images
    """
    image_url = request.args.get('image_url')
    print(image_url)
    if "https://i.scdn.co" in image_url:
        image = requests.get(image_url)
        return (image.content, 200, {'Content-Type': 'image/jpeg'})
    else:
        return None


app.run(host='0.0.0.0', port=8080, debug=True)