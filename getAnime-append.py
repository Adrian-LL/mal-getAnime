'''
This script can be used to download anime dataset from [**Myanimelist**](https://myanimelist.net/) using an unofficial MyAnimeList REST API, [**Jikan**](https://jikan.me/docs).
Column metadata:

animeID: id of anime as in anime url https://myanimelist.net/anime/ID
name: title of anime
premiered: premiered on. default format (season year) 
genre: list of genre
type: type of anime (example TV, Movie etc) 
episodes: number of episodes
studios: list of studio
source: source of anime (example original, manga, game etc) 
scored: score of anime
scoredBy: number of member scored the anime
members: number of member added anime to their list
rank: TBD
popularity: TBD

TO BE UPDATED
'title', 
'title_english', 
'title_japanese', 
'title_synonyms',
'image_url', 
'type', 
'source', 
'episodes', 
'status', 
'airing',
'aired_string', 
'aired', 
'duration', 
'rating', 
'score', 
'scored_by',
'rank', 
'popularity', 
'members', 
'favorites', 
'background', 
'premiered',
'broadcast', 
'related', 
'producer', 
'licensor', 
'studios', 
'genres',
'opening_theme', 
'ending_theme', 
'aired_from_year', 
'genre'

'''

# importing libraries
import requests
import json
import csv
import sys
import time

count = 0 # keep count of anime	for current session

# Command line arguments try
try:
	start = int(sys.argv[1]) # starting index
	end = int(sys.argv[2]) + 1 # ending index
except IndexError:
	print('Please provide all arguments.\nSyntax:\npython getAnime.py starting_index ending_index [output_file.csv]')
	sys.exit()
except:
	print('Unexpected error.')

# setting name of output files
if(len(sys.argv) == 4):
	outputFile = str(sys.argv[3])
	errorFile = str(sys.argv[3] + '_errors.csv')
else:
	outputFile = 'Anime.csv'
	errorFile = 'Anime.csv_errors.csv'

# opening output file for *appending*
# don't forget the encoding for japanese and or other unicode caracters
# please note the newline = '' - it is needed only for Windows (otherwise writer insert blank rows)
w = open(outputFile, 'a', encoding='utf-8', newline = '')
e = open(errorFile, 'a', encoding='utf-8', newline = '')

# header
# commented because this is the append file
# w.write('animeID, name, title_english, title_japanese, title_synonyms, type, source, producers, genres, studios, episodes, status, airing, aired, duration, rating, score, scored_by, ranked, popularity, members, favorites, synopsis, background, premiered, broadcast, related\n')

# creating csv writer objects
writer = csv.writer(w)
error_writer = csv.writer(e)

# Main loop to crawl the anime indexes

for i in range(start, end): # note: The index starts in 1 and ends in 37115 (as on Jan 15 2018)
	# jikan api - to be cheked because it updates periodically
	# documentation at https://jikan.docs.apiary.io/#
	# i is the index of anime such as https://myanimelist.net/anime/i
	apiUrl = 'https://api.jikan.moe/v3/anime/' + str(i)

	# wait 4 seconds for avoiding API throttling problems (see jukan docs)
	time.sleep(4)
	
	# First API call for the current i index
	page = requests.get(apiUrl)
	
	# Printing status to output
	print('\n1. Index =', i)
	print('2. Page status code =', page.status_code)
	
	# Ckeck if 404 erro (page not found)
	while page.status_code != 404:
	
		# Debugging
		print('Let\'s see if we get there')
		
		# processing 429 (too many requests) errors
		if page.status_code == 429:
			print('    2\'. (wait + retry) ')
			# sleep 15 seconds
			time.sleep(15)
			#repeat API call
			page = requests.get(apiUrl)
			if page.status_code != 200:
				print('    2\'. After retrying page status code =', page.status_code)
				# Initializing error list
				err_l = []
				# Append to error list
				err_l.append(i)
				err_l.append(page.status_code)
				err_l = [err_l] # helps with csv writerows
				error_writer.writerows(err_l) # write one line in errors csv
			
		# print(page.content) # debugging
		
		# Creating and Decoding JSON
		try:
			print('3. Fetching JSON...', i)
			# this goes rather here
			# c = page.content # (redundant)
			# jsonData = json.loads(c)
			jsonData = json.loads(page.content)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			continue

		# if status code is 200 then write to file
		# NOTE - to do something with other codes
		# e.g if status code != 404 sleep(5) then retry
		
		if(page.status_code == 200):
			
			# NOTE - if not 404 or not 200 the count will not increase
			# And will go back to while loop

			count = count + 1 # Increment anime count

			print('\nWriting to file...') # Message

			l = [] # List to store the data to write

			name = jsonData['title'] # getting anime title

			print('Reading', name, 'animelist...') # printing title to screen

			studio = [] # list to store studio (list cause it can be more then 1)
			genre = [] # list to store genre (list cause it can be more then 1)
			
			producers = [] # idem
			licensors = [] # idem

			# aired_string = [] # list to store aired properties (can be more than 1)

			# getting studio name
			for j in range(0, len(jsonData['studios'])):
				studio.append(jsonData['studios'][j]['name'])

			# getting genre
			for j in range(0, len(jsonData['genres'])):
				genre.append(jsonData['genres'][j]['name'])

			# getting producers
			for j in range(0, len(jsonData['producers'])):
				producers.append(jsonData['producers'][j]['name'])

			# getting licensors
			for j in range(0, len(jsonData['licensors'])):
				licensors.append(jsonData['licensors'][j]['name'])

			# added
			# for j in range(0, len(jsonData['aired'])):
			# 	aired_string.append(jsonData['aired'][j]['string'])	

			l.append(i) # anime ID
			l.append(name) # anime title - extracted from json above
			# added 2019-01-25
			l.append(jsonData['title_english'])
			l.append(jsonData['title_japanese'])
			l.append(jsonData['title_synonyms'])
			l.append(jsonData['type']) # anime type
			l.append(jsonData['source']) # source of anime
			# extracted data
			l.append(producers) # list of strings: producers, extracted above
			l.append(genre) # list of strings: anime genre, extracted above
			l.append(studio) # list of strings: studio, extracted above
			# other data
			l.append(jsonData['episodes']) # number of episodes
			l.append(jsonData['status']) # aired or not etc. (added 2019-01-25)
			l.append(jsonData['airing']) # True or False
			l.append(jsonData['aired']) # dictionary with aired dates
			l.append(jsonData['duration']) # per episode or the entire duration if movie
			l.append(jsonData['rating']) # age rating
			l.append(jsonData['score']) # score 0 to 10
			l.append(jsonData['scored_by']) # number of users that scored
			l.append(jsonData['rank']) # weighted according to some MAL formula
			l.append(jsonData['popularity']) # based on how many members/users have the repective anime in their list
			l.append(jsonData['members']) # number members added this anime in their list
			l.append(jsonData['favorites']) # TBD number members that favitest these in their list
			l.append(jsonData['synopsis']) # long string with anime synopsis
			l.append(jsonData['background']) # long string with production background and other things
			l.append(jsonData['premiered']) # anime premiered on
			l.append(jsonData['broadcast']) # when is (regularly) broadcasted
			l.append(jsonData['related']) # dictionary: related animes, series, games etc.
			
			
			# preparing to write csv
			l = [l] # help in writing using csv.writer.writerows

			print('Writing anime', name)
			print('Total Anime stored in  the session:', count)
			print('Index of anime to be written:', i, '\n')

			writer.writerows(l) # writing one row in the CSV

			# if we get there, break the `while != 404` loop
			# while loops can be dangerous!!!
			# if also not 200, it will not reach there, so go back to `while`
			break

w.close() # closing main csv file
e.close() # close also errors file

print('No more anime left. Done.\nOutput file:', outputFile)
print('Error file', errorFile)