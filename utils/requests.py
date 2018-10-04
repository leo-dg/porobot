import urllib.request
import json
from utils import config


class Riotwrapper():

    def __init__(self):
        self._REGION = 'euw1'  # TODO: Implement multiple-region compatiblity.
        self._URL_PREFIX = f"https://{self._REGION}.api.riotgames.com"
        self._URL_SUFFIX = f"?api_key={config.keys['riot_api_key']}"
        self._got_champdd = False
        self._champdd = {}

    def send_request(self, url):
        with urllib.request.urlopen(url) as urlstr:
            if urlstr.getcode() != 200:
                return "ERROR"
            _res = str(urlstr.read().decode('utf-8'))
        return json.loads(_res)

    def get_latest_dd(self):
        _vurl = "https://ddragon.leagueoflegends.com/api/versions.json"
        _latest_ver = self.send_request(_vurl)[0]
        return _latest_ver

    def get_champ(self, champ_id):
        '''
        ** could have more efficient searching
        _champdata to get data about champ_id
        => name, url for thumbnail
        '''
        if not self._got_champdd:
            # Get latest API version for DD.
            _champdd_url = f"http://ddragon.leagueoflegends.com/cdn/{self.get_latest_dd()}/data/en_GB/champion.json"
            self._champdd = self.send_request(_champdd_url)
            self._got_champdd = True

        for champ in self._champdd['data']:
            if int(self._champdd['data'][champ]['key']) == int(champ_id):
                _champ_data = {
                    "name": self._champdd['data'][champ]['name'],
                    "champ_pfp_url": f"http://ddragon.leagueoflegends.com/cdn/{self.get_latest_dd()}/img/champion/{self._champdd['data'][champ]['image']['full']}"
                }
                return _champ_data

    def get_status(self):
        '''
        Gets the status of Riot components.
        => dict object of statuses.
        '''
        _url = f"{self._URL_PREFIX}/lol/status/v3/shard-data{self._URL_SUFFIX}"
        _resobj = self.send_request(_url)
        _services = _resobj['services']
        _status = {
            "region": _resobj['name'],
            "game_status": _services[0]['status'],
            "store_status": _services[1]['status'],
            "web_status": _services[2]['status'],
            "client_status": _services[3]['status'],
        }
        return _status

    def get_match_info(self, match_id, user_id):
        '''
        Extra match info.
        => dict object of match.
        '''
        _url = f"{self._URL_PREFIX}/lol/match/v3/matches/{match_id}{self._URL_SUFFIX}"
        _resobj = self.send_request(_url)

        # get correct participantId
        for ptp_identity in _resobj['participantIdentities']:
            if ptp_identity['player']['accountId'] == user_id:
                # match with 'participants' data
                ptp_id = ptp_identity['participantId']
                break

        # get player specific match data from obj array 'participants'
        for ptp in _resobj['participants']:
            if ptp['participantId'] == ptp_id:
                _lastmatch_info = {
                    "map": config.MAPS[str(_resobj['mapId'])],
                    "game_mode": _resobj['gameMode'],
                    "team_id": ptp['teamId'],
                    "result": ':trophy: Victory' if ptp['stats']['win'] else ':skull_crossbones: Defeat',
                    "kda": f":crossed_swords: {ptp['stats']['kills']} | :skull: {ptp['stats']['deaths']} | :busts_in_silhouette: {ptp['stats']['assists']}"
                }
                return _lastmatch_info

    def get_lastmatch_info(self, user_id):
        '''
        Gets last match info with specfic user id.
        => dict object of last match.
        '''
        _url = f"{self._URL_PREFIX}/lol/match/v3/matchlists/by-account/{user_id}{self._URL_SUFFIX}&endIndex=1"
        _resobj = self.send_request(_url)

        _match_info = {
            "match_count": _resobj['totalGames'],
            "champ": _resobj['matches'][0]['champion'],
            "lane": _resobj['matches'][0]['lane'].lower().capitalize() if _resobj['matches'][0]['lane'] != "NONE" else 'Unspecified',
            "role": _resobj['matches'][0]['role'].lower().capitalize() if _resobj['matches'][0]['role'] != "NONE" else 'Unspecified'
        }

        _match_id = _resobj['matches'][0]['gameId']
        _extra_match_info = self.get_match_info(_match_id, user_id)
        _match_info.update(_extra_match_info)  # Merge dictionary objs.
        return _match_info

    def get_user_info(self, user):
        '''
        Gets info about a username string input.
        => dict object of user data.
        '''
        _url = f"{self._URL_PREFIX}/lol/summoner/v3/summoners/by-name/{user}{self._URL_SUFFIX}"
        try:
            _resobj = self.send_request(_url)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("=== 404 ERROR IN REQUEST ===")
                return -1

        _user = {
            "user_name": _resobj['name'],
            "pfp_url": f"http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/{_resobj['profileIconId']}.png",
            "user_level": _resobj['summonerLevel'],
            "user_id": _resobj['accountId']
        }

        return _user
