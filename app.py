from flask import render_template
from flask import request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

from flask import Flask
app = Flask(__name__)

user = 'ubuntu' #add your username here (same as previous postgreSQL)        $
host = 'localhost'
dbname = 'reco_db'
db = create_engine('postgresql://ubuntu:ubuntu@localhost:5432/%s'%(dbname))
#engine = create_engine('postgresql://matt-666:matt-666@localhost:5432/%s' % my$

con = None
#con = psycopg2.connect(database = dbname, user = user)
con = psycopg2.connect(dbname = dbname, user = user, host='localhost', password = 'everything')

@app.route('/help')
def help():
    return render_template("output.html", sids = [dict(artist_name='bob',title='bob')])

@app.route('/db')
def birth_page():
    sql_query = """                                                            
                SELECT song_metadata.artist_name, song_metadata.title 
		FROM reco_table2
                INNER JOIN song_metadata
                ON reco_table2.song_id = song_metadata.song_id
                LIMIT 10
                ;
                """
                #WHERE reco_table.artist_name='Metallica';
    query_results = pd.io.sql.read_sql(sql_query,con)
    sids = ""
    sids2 = []
    for i in range(0,10):
        sids += str(query_results.iloc[i]['artist_name'])
        sids += str(query_results.iloc[i]['title'])
        sids += "<br>"
        sids2.append(dict(artist_name=query_results.iloc[i]['artist_name']))
    
    return render_template("output.html", sids=sids2)


@app.route('/')
@app.route('/input')
def ces_input():
   return render_template("input.html")

@app.route('/test')
def test1():
    return(request.args.get('artist_name'))

@app.route('/output')
def ces_ouput():
    #pull 'birth_month' from input field and store it
    artist_name = request.args.get('artist_name')
    instrument1 = request.args.get('bandmate1')
    #instrument2 = request.args.get('bandmate2')
    #instrument3 = request.args.get('bandmate3')
    skill1 = request.args.get('skill-bandmate1')
    #skill2 = request.args.get('skill-bandmate2')
    #skill3 = request.args.get('skill-bandmate3')
    #print(instrument1)    
    #print(skill1)
    #print(artist_name)
    types = []
    #instrs = [instrument1, instrument2, instrument3]
    instrs = instrument1	
    if any([instr == 'guitar' for instr in instrs]):
        types.extend(['Chords', 'Tabs'])
 
    if any([instr == 'Bass Tabs' for instr in instrs]):
        types.extend(['Bass Tabs', 'other'])

    if any([instr == 'Drum Tabs' for instr in instrs]):
        types.extend(['Drum Tabs', 'other'])

    types = tuple(types)
    #print(types)
    if artist_name:
	query = """
                SELECT song_metadata.artist_name, song_metadata.title 
                FROM reco_table2
                INNER JOIN song_metadata
                ON reco_table2.song_id = song_metadata.song_id
                LIMIT 10
                ;
		"""
    #if artist_name:
    #    query = """SELECT song_metadata.artist_name, song_metadata.title, 
    #               scraped_info2.tab_type, scraped_info2.chords,
    #               scraped_info2.song_links, reco_table2.scores
    #               FROM reco_table2 
    #               INNER JOIN song_metadata 
    #               ON song_metadata.song_id = reco_table2.song_id
    #               INNER JOIN scraped_info2
    #               ON reco_table2.song_id = scraped_info2.song_id
    #               WHERE reco_table2.artist_name='%s' 
    #               AND scraped_info2.tab_type IN %s
    #               AND scraped_info2.predicted_difficulty = '%s'
    #               ORDER BY reco_table2.scores DESC
    #               LIMIT 10;""" % (artist_name, types, skill1)
    else:
        query = """SELECT DISTINCT song_metadata.artist_name, song_metadata.title,
                   scraped_info2.tab_type, scraped_info2.chords, 
                   scraped_info2.song_links
                   FROM reco_table2 
                   INNER JOIN song_metadata 
                   ON song_metadata.song_id = reco_table2.song_id
                   INNER JOIN scraped_info2
                   ON reco_table2.song_id = scraped_info2.song_id
                   WHERE scraped_info2.tab_type IN %s
                   AND scraped_info2.predicted_difficulty = '%s'
                   LIMIT 10;""" % (types, skill1)
    query_results = pd.io.sql.read_sql(query,con)
    #print query_results
    sids = []
    for i in range(0,query_results.shape[0]):
        sids.append(dict(artist_name = query_results.iloc[i]['artist_name'], \
                         title = query_results.iloc[i]['title'], \
                         tab_type = query_results.iloc[i]['tab_type'], \
                         difficulty = query_results.iloc[i]['predicted_difficulty'], \
                         link = query_results.iloc[i]['song_links'],\
                         chords = query_results.iloc[1]['chords']))
    #    the_result = ''
    #the_result = ModelIt(patient,births, the_result = the_result)
    return render_template("output.html", sids = sids, section = "features")






if __name__ == '__main__':
  app.run()
