"""
Taken from: https://raw.githubusercontent.com/PaulSec/API-EZTV.it/master/eztv_api.py
---

This is the (unofficial) Python API for EZTV.it

Using this code, you can manage to get the information regarding any TV Show
which is listed on EZTV.it See how to use it thanks to the file "APIExample.py"

"""
from bs4 import BeautifulSoup
import requests
import re

URL = "https://eztv.ch"
QUALITY_PREF = "460p"


class EztvException(Exception):
    """
        Base exception for this API
    """

    def __init__(self, message, errors):
        """
            Class constructor
        """

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.errors = errors


class TVShowNotFound(EztvException):
    """
        TV Show Not Found Exception
    """


class SeasonNotFound(EztvException):
    """
        Season Not Found Exception
    """


class EpisodeNotFound(EztvException):
    """
        Episode Not Found Exception
    """


class EztvAPI(object):
    """
        EztvAPI Main Handler
    """

    _instance = None
    _id_tv_show = None
    _season_and_episode = {}
    _patterns = [
        r"S(\d+)E(\d+)",  # Matches SXXEYY (eg. S01E10)
        r"(\d+)x(\d+)",  # Matches SSxYY (eg. 01x10)
    ]

    def __new__(cls, *args, **kwargs):
        """
            __new__ builtin
        """
        if not cls._instance:
            cls._instance = super(EztvAPI, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def _match_pattern(self, pattern, episode):
        regex = re.search(pattern, episode)
        if regex is None:  # Yeah, I try to be a positive person.
            return

        season_tv_show = regex.group(1)
        episode_tv_show = regex.group(2)
        regex = re.search(r"href=\"([^\"]*)\" ", episode)
        magnet_link = regex.group(1)

        return (season_tv_show, episode_tv_show, magnet_link)

    def tv_show(self, name):
        """
            Fetches a show mapping $name returns a $self instance.
            Might raise a TVShowNotFound exception
        """
        # all strings are in lowercase
        name = name.lower()
        terms = name.split(' ')

        req = requests.get(URL, timeout=5, verify=False)

        soup = BeautifulSoup(req.content, 'html.parser')
        tv_shows = str(
            soup('select', {'name': 'SearchString'})).split('</option>')
        for tv_show in tv_shows:
            tv_show = tv_show.lower()
            if all(x in tv_show for x in terms):
                # get the id of the show
                id_tv_show = re.search(r"value=\"(\d+)\"", tv_show)
                self._id_tv_show = id_tv_show.group(1)
                break

        else:
            raise TVShowNotFound('The TV Show "%s" has not been found.'
                                 % ' '.join(terms), None)

        # load the tv show data
        self.load_tv_show_data()
        return self._instance

    def load_tv_show_data(self):
        """
            load the data, create a dictionary structure with all seasons,
            episodes, magnet.
        """

        url = "{}/search/".format(URL)
        payload = {'SearchString': self._id_tv_show,
                   'SearchString1': '', 'search': 'Search'}

        req = requests.post(url, data=payload, timeout=5, verify=False)
        soup = BeautifulSoup(req.content, 'html.parser')

        self._season_and_episode = {}
        episodes = str(soup('a', {'class': 'magnet'})).split('</a>')
        for epi in episodes:
            for pat in self._patterns:
                data = self._match_pattern(pat, epi)
                if data is None:
                    continue
                self.add_season_and_episode(data[0], data[1], data[2])
        return self._instance

    def add_season_and_episode(self, num_season, num_episode, magnet_link):
        """
             insert into the dictionary the season and the episode with the
             specific magnet link 
             but also consider quality preference (QUALITY_PREF)
        """
        num_season = int(num_season)
        num_episode = int(num_episode)
        magnet_link = magnet_link.replace('&amp;', '&')

        if (num_season not in self._season_and_episode):
            self._season_and_episode[num_season] = {}

        if (num_episode not in self._season_and_episode[num_season]):
            self._season_and_episode[num_season][num_episode] = magnet_link
        elif (QUALITY_PREF in magnet_link):
            self._season_and_episode[num_season][num_episode] = magnet_link

        return self._instance

    def episode(self, num_season=None, num_episode=None):
        """
             specific episode
             return magnet link of episode
             might raise SeasonNotFound or EpisodeNotFound exceptions
        """
        # specific episode
        if (num_season is not None and num_episode is not None):
            # verifiyng the season exist
            if (num_season not in self._season_and_episode):
                raise SeasonNotFound(
                    'The season %s does not exist.' % num_season, None)

            # verifying the episode exists
            if (num_episode not in self._season_and_episode[num_season]):
                raise EpisodeNotFound(
                    'The episode %s does not exist.' % num_episode, None)

            return self._season_and_episode[num_season][num_episode]

    def season(self, num_season=None):
        """
             specifc season
             return data structure (dictionary)
             might raise SeasonNotFound exceptions
        """
        # specific season, all episodes
        if (num_season is not None):
            # verifiyng the season exist
            if (num_season not in self._season_and_episode):
                raise SeasonNotFound(
                    'The season %s does not exist.' % num_season, None)

            return self._season_and_episode[num_season]

        # all seasons
        else:
            return self._season_and_episode

    def seasons(self):
        """
            all seasons
        """
        return self._season_and_episode

    def update(self):
        """
            load the data, create a dictionary structure with all seasons,
            episodes, magnet.
        """
        return self.load_tv_show_data()