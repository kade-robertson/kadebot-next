# Movie plugin
# Commands:
#   - /movie
#   - /moviesearch
# Configuration:
# command.movie:
#   api_key: "OMDb API key"
#   fanart_key: "Optional - Fanart API key"
#   fanart_ckey: "Optional - Fanart API client key"


import re
import omdb
import shlex
import requests
from .basic import *

class Movie(CommandBase):
    name = 'Movie'
    safename = 'movie'
    def __init__(self, logger):
        super().__init__(logger)
        self.idmatch = re.compile('tt[0-9]{7}')
        self.to_register = [
            CommandInfo("movie", self.execute_movie, "Displays movie information."),
            CommandInfo("moviesearch", self.execute_search, "Searches for a movie.")
        ]
    def load_config(self, confdict):
        self.api = omdb.OMDBClient(apikey = confdict["api_key"])
        self.artkey = confdict['fanart_key'] 
        self.artckey = confdict['fanart_ckey'] 
    def get_help_msg(self, cmd):
        if cmd == "movie":
            return 'Call /movie <id> with the IMDb ID of the movie you want information for.'
        elif cmd == "moviesearch":
            return ('Call /moviesearch <search> with the title you wish to search for, '
                    'using quotes if there are spaces.')
    @bot_command
    def execute_movie(self, bot, update, **kwargs):
        args = kwargs.get('args')
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /movie.",
                             disable_notification = True)
            return
        is_movie = self.idmatch.findall(args[0])
        if not is_movie or len(is_movie) == 0:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "That doesn't look like a proper IMDb ID.",
                             disable_notification = True)
            return
        movie = self.api.get(imdbid = is_movie[0])
        output = 'Movie: <a href="http://www.imdb.com/title/{}/">{}</a> ({})\n'.format(movie['imdb_id'], movie['title'], movie['released']) + \
                 "Director(s): {}\n".format(movie['director']) + \
                 "Actors: {}\n".format(movie['actors']) + \
                 "IMDB Score: {} ({} votes)\n".format(movie['imdb_rating'], movie['imdb_votes']) + \
                 "Metascore: {}\n".format(movie['metascore']) + \
                 "Awards: {}\n\n".format(movie['awards']) + movie['plot']

        if self.artkey and self.artckey:
            images = requests.get(
                'http://webservice.fanart.tv/v3/movies/{}'.format(movie['imdb_id']),
                params = { 'api_key': self.artkey, 'client_key': self.artckey }
            ).json()
            if 'movieposter' in images:
                english_posters = [poster for poster in images['movieposter'] if poster['lang'] == 'en']
                bot.send_photo(chat_id = update.message.chat_id,
                               photo = english_posters[0]['url'],
                               disable_notification = True)
            elif movie['poster'] != "N/A" and requests.get(movie['poster']).status_code == 200:
                bot.send_photo(chat_id = update.message.chat_id,
                               photo = movie['poster'],
                               disable_notification = True)
        bot.send_message(chat_id = update.message.chat_id,
                         text = output,
                         parse_mode = 'HTML',
                         disable_notification = True,
                         disable_web_page_preview = True)
    @bot_command
    def execute_search(self, bot, update, **kwargs):
        args = kwargs.get('args')
        if len(args) != 1:
            bot.send_message(chat_id = update.message.chat_id,
                             text = "This doesn't seem like correct usage of /moviesearch.",
                             disable_notification = True)
            return
        results = self.api.get(search = args[0])
        output = "Results:\n"
        for res in results[:7]:
            output += " - {} ({}): {}\n".format(res['title'], res['year'], res['imdb_id'])
        bot.send_message(chat_id = update.message.chat_id,
                         text = output,
                         disable_notification = True)
