# mal-getAnime
Pyhton script for getting anime from MyAnimeList / forked from Dibakarroy1997/myanimelist-data-set-creator
## Two files
1. `getAnime.py` - for getting the first x rows. Creates the output file and writes the headers.
2. `getAnime-append.py` - for appending the next rows to an already existing `.csv`, without headers

# Done
* Modified the link to `jikan` API.
* Added some more fields to json
* Added utf-8 encoding to output file
* corrected `jsonData` variable whose definition was missing

# TO DO
* update `getAnime-append.py`
* to append to file instead of write (open('w')). To fiddle to check if the file exists etc.
* to get more fields from the MAL page (e.g japanese name etc. - only if useful)
