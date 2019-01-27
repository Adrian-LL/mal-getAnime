# mal-getAnime
Pyhton script for getting anime from MyAnimeList.

Based on **jikan** unofficial API (https://jikan.docs.apiary.io/) 

Forked from Dibakarroy1997/myanimelist-data-set-creator (https://github.com/Dibakarroy1997/myanimelist-data-set-creator).

>Please note that because a site is crawled with an unofficial API, not all the pages are fetched. Sometimes there are errors which are not catched by the script.

## Two files
1. `getAnime.py` - for getting the first x rows. Creates the output file and writes the headers. The file is opened in `'w'` (write) mode. 
> An existing file is overwritten.

Usage:
```bash
$ python getAnime.py index_start index_stop <file_name> # (default Anime.csv>)
```


2. `getAnime-append.py` - for appending the next rows to an already existing `.csv`, without headers. The file is opened in `'a'` (append) mode. Default `Anime.csv`. An existing file is NOT overwritten.


Usage:
```bash
$ python getAnime-append.py index_start index_stop <file_name> # (default Anime.csv>)
```
> NOTE - the output is encoded in `utf-8`.

# Done
* Modified the link to `jikan` API.
* Added some more fields to json
* Added utf-8 encoding to output file
* corrected `jsonData` variable whose definition was missing

# Fields (Columns) of Dataset

See also code.
 
```python
'animeID'       # anime ID
'name'          # anime title - extracted from json above
'title_english' # title in English
'title_japanese' # title in Japanese
'title_synonyms' # other variants of title
'type'          # anime type (TV, Movie, OVA)
'source'        # source of anime (i.e orginal, manga, game)
# extracted data
'producers'     # list of strings: producers, extracted above
'genres'        # list of strings: anime genre, extracted above
'studios'       # list of strings: studio, extracted above
# other data
'episodes'      # number of episodes
'status'        # aired or not etc. (added 2019-01-25)
'airing'        # True or False
'aired'         # dictionary with aired dates
'duration'      # per episode or the entire duration if movie
'rating'        # age rating
'score'         # score 0 to 10
'scored_by'     # number of users that scored
'rank'          # weighted according to some MAL formula
'popularity'    # based on how many members/users have the repective anime in their list
'members'       # number members added this anime in their list
'favorites'     # TBD number members that favitest these in their list
'synopsis'      # long string with anime synopsis
'background'    # long string with production background and other things
'premiered'     # anime premiered on
'broadcast'     # when is (regularly) broadcasted
'related'       # dictionary: related animes, series, games etc.
```
