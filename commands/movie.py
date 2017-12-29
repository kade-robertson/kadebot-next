import re
import omdb
import shlex
import requests
from .basic import CommandBase

class Movie(CommandBase):
    name = 'Movie'
    safename = 'movie'
    def __init__(self, logger):
        super().__init__(logger)
        self.idmatch = re.compile('tt[0-9]{7}')
        self.to_register = [("movie", self.execute_movie, "Displays movie information."),
                            ("moviesearch", self.execute_search, "Searches for a movie.")]
    def load_config(self, confdict):
        self.api = omdb.Client(apikey = confdict["api_key"])
    def get_help_msg(self, cmd):
        if cmd == "movie":
            return 'Call /movie <id> with the IMDb ID of the movie you want information for.'
        elif cmd == "moviesearch":
            return 'Call /moviesearch <search> with the title you wish to search for, using quotes if there are spaces'
    def execute_movie(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 2:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /movie.",
                                 disable_notification = True)
                return
            is_movie = self.idmatch.match(args[1])
            if not is_movie:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "That doesn't look like a proper IMDb ID.",
                                 disable_notification = True)
                return
            movie = self.api.get(imdbid = args[1])
            output = "Movie: {} ({})\n".format(movie.title, movie.year) + \
                     "Director(s): {}\n".format(movie.director) + \
                     "Actors: {}\n".format(movie.actors) + \
                     "IMDB Score: {} ({} votes)\n".format(movie.imdb_rating, movie.imdb_votes) + \
                     "Metascore: {}\n".format(movie.metascore) + \
                     "Awards: {}\n\n".format(movie.awards) + movie.plot
            if movie.poster != "N/A" and requests.get(movie.poster).status_code == 200:
                bot.send_photo(chat_id = update.message.chat_id,
                               photo = movie.poster,
                               disable_notification = True)
            bot.send_message(chat_id = update.message.chat_id,
                             text = output,
                             disable_notification = True)
            self.logger.info("Command /movie completed successfully.")
        except Exception as e:
            self.logger.exception(e)
    def execute_search(self, bot, update):
        try:
            args = shlex.split(update.message.text)
            if len(args) != 2:
                bot.send_message(chat_id = update.message.chat_id,
                                 text = "This doesn't seem like correct usage of /movie.",
                                 disable_notification = True)
                return
            results = self.api.get(search = args[1])
            output = "Results:\n"
            for res in results[:7]:
                output += " - {} ({}): {}\n".format(res.title, res.year, res.imdb_id)
            bot.send_message(chat_id = update.message.chat_id,
                             text = output,
                             disable_notification = True)
            self.logger.info("Command /moviesearch completed successfully.")
        except Exception as e:
            self.logger.exception(e)