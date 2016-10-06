# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 21:04:54 2016

@author: matt-666
"""

from flask_files import app
from flask import render_template
from flask import request 
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

def removeTags(string):
    '''
    Function to remove html tags
    '''
    return re.sub('<[^<]+?>', '', string)


user = 'ubuntu' #add your username here (same as previous postgreSQL)                      
host = 'localhost'
dbname = 'reco_db'
db = create_engine('postgresql://ubuntu:ubuntu@localhost:5432/%s'%(dbname))
#engine = create_engine('postgresql://matt-666:matt-666@localhost:5432/%s' % mydbname)

con = None
#con = psycopg2.connect(database = dbname, user = user)
con = psycopg2.connect(dbname = dbname, user = user, host='localhost', password='matt')

artist_query = "SELECT DISTINCT artist_name FROM reco_table2;"
artist_query_results = pd.io.sql.read_sql(artist_query,con)
unique_artists = []
for i in range(0, artist_query_results.shape[0]):
    unique_artists.append(artist_query_results.iloc[i]['artist_name'])
unique_artists = sorted(unique_artists)


@app.route('/index')
def index():
   return render_template("index.html", unique_artists = unique_artists)
   #return "Hello, World!"
   
@app.route('/')
@app.route('/input')
def ces_input():
   return render_template("input.html", unique_artists = unique_artists)
   #return "Hello, World!"

@app.route('/model-details')
def model_details():
    return render_template("model-details.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/output')
def ces_ouput():
    baseurl = 'https://www.ultimate-guitar.com'

    now = datetime.now()
    ugpage = requests.get('https://www.ultimate-guitar.com/updates/?filter=tabs&date=%s-%s-%s'%(now.year, now.month, now.day-1))
    bs = BeautifulSoup(ugpage.content)
    artists = [removeTags(str(artist)).strip().decode('utf-8') for artist in bs.find_all('td', {'width':'35%'})]
    artist_links = [baseurl+artist_n.find('a')['href'] for artist_n in bs.find_all('td', {'width':'35%'})]
    titles = [removeTags(str(title)).strip().decode('utf-8') for title in bs.find_all('td', {'width':'50%'})]
    title_links = [str(title_n.find('a')['href']).decode('utf-8') for title_n in bs.find_all('td', {'width':'50%'})]
    #print('tt', title_links)
    types = [removeTags(str(type_)).replace('[','').replace(']','').strip().decode('utf-8') for type_ in bs.find_all('td', {'width':'15%', 'valign':'top'})]

    if len(types)>=10:
        new_songs = [dict(artist=artists[i], artist_link = artist_links[i], title_link = title_links [i], \
                    title = titles[i], thetype = types[i]) for i in range(len(types)-1, len(types)-11, -1)]
    else:
        new_songs = [dict(artist=artists[i], artist_link = artist_links[i], title_link = title_links [i], \
                    title = titles[i], thetype = types[i]) for i in range(len(types))]

    #pull 'birth_month' from input field and store it
    artist_name = request.args.get('artist_name')
    instrument1 = request.args.get('bandmate1')
    instrument2 = request.args.get('bandmate2')
    instrument3 = request.args.get('bandmate3')
    skill1 = request.args.get('skill-bandmate1')
    skill2 = request.args.get('skill-bandmate2')
    skill3 = request.args.get('skill-bandmate3')
    if skill1 == 'novice':
        skill = ('novice', 'other')
    elif skill1 == 'intermediate':
        skill = ('novice', 'intermediate')
    elif skill1 == 'advanced':
        skill = ('novice', 'intermediate', 'advanced')
    else:
        skill = ('novice', 'other')
    
    types = []
    instrs = [instrument1, instrument2, instrument3]
    
    if any([instr == 'guitar' for instr in instrs]):
        types.extend(['Chords', 'Tabs'])
        
    if any([instr == 'Bass Tabs' for instr in instrs]):
        types.extend(['Bass Tabs', 'other'])    
        
    if any([instr == 'Drum Tabs' for instr in instrs]):
        types.extend(['Drum Tabs', 'other'])    
        
    types = tuple(types)
    #print(types)
    if artist_name:
        query = """SELECT song_metadata.artist_name, song_metadata.title, 
                   scraped_info2.tab_type, scraped_info2.chords,scraped_info2.difficulty,
                   scraped_info2.song_links, reco_table2.scores
                   FROM reco_table2 
                   INNER JOIN song_metadata 
                   ON song_metadata.song_id = reco_table2.song_id
                   INNER JOIN scraped_info2
                   ON reco_table2.song_id = scraped_info2.song_id
                   WHERE reco_table2.artist_name='%s' 
                   AND scraped_info2.tab_type IN %s
                   AND scraped_info2.difficulty IN %s
                   ORDER BY reco_table2.scores DESC
                   LIMIT 10;""" % (artist_name, types, skill)
    else:
        query = """SELECT DISTINCT song_metadata.artist_name, song_metadata.title, 
                   scraped_info2.tab_type, scraped_info2.chords, scraped_info2.difficulty,
                   scraped_info2.song_links, reco_table2.scores
                   FROM reco_table2 
                   INNER JOIN song_metadata 
                   ON song_metadata.song_id = reco_table2.song_id
                   INNER JOIN scraped_info2
                   ON reco_table2.song_id = scraped_info2.song_id
                   WHERE scraped_info2.tab_type IN %s
                   AND scraped_info2.difficulty IN %s
                   ORDER BY reco_table2.scores DESC
                   LIMIT 10;""" % (types, skill)

    query_results = pd.io.sql.read_sql(query,con)
    
    sids, chords = [], []
    for i in range(0,query_results.shape[0]):
        sids.append(dict(artist_name = query_results.iloc[i]['artist_name'], \
                         title = query_results.iloc[i]['title'], \
                         tab_type = query_results.iloc[i]['tab_type'], \
                         difficulty = query_results.iloc[i]['difficulty'], \
                         link = query_results.iloc[i]['song_links'],\
                         score = round(query_results.iloc[i]['scores'], 4), \
                         chords = query_results.iloc[i]['chords']\
                         ))
        chords.append(query_results.iloc[i]['chords'])
    
    return render_template("output.html", unique_artists = unique_artists, sids = sids, chords = chords, new_songs = new_songs, section = "features")
    
