import os, json
import requests
import inspect
import logging
import httplib

logger = logging.getLogger(__name__)
champ_map = {
    "Wukong": "62",
    "Jax": "24",
    "Shaco": "35",
    "Warwick": "19",
    "Nidalee": "76",
    "Zyra": "143",
    "Brand": "63",
    "Rammus": "33",
    "Illaoi": "420",
    "Corki": "42",
    "Braum": "201",
    "Anivia": "34",
    "Tryndamere": "23",
    "Miss Fortune": "21",
    "Blitzcrank": "53",
    "Yorick": "83",
    "Xerath": "101",
    "Sivir": "15",
    "Riven": "92",
    "Orianna": "61",
    "Gangplank": "41",
    "Malphite": "54",
    "Poppy": "78",
    "Karthus": "30",
    "Jayce": "126",
    "Nunu": "20",
    "Trundle": "48",
    "Sejuani": "113",
    "Graves": "104",
    "Lucian": "236",
    "Gnar": "150",
    "Lux": "99",
    "Shyvana": "102",
    "Renekton": "58",
    "Fiora": "114",
    "Jinx": "222",
    "Kalista": "429",
    "Fizz": "105",
    "Kassadin": "38",
    "Sona": "37",
    "Irelia": "39",
    "Viktor": "112",
    "Kindred": "203",
    "Cassiopeia": "69",
    "Maokai": "57",
    "Thresh": "412",
    "Kayle": "10",
    "Hecarim": "120",
    "Kha'Zix": "121",
    "Olaf": "2",
    "Ziggs": "115",
    "Syndra": "134",
    "Dr. Mundo": "36",
    "Karma": "43",
    "Annie": "1",
    "Akali": "84",
    "Leona": "89",
    "Yasuo": "157",
    "Kennen": "85",
    "Rengar": "107",
    "Ryze": "13",
    "Shen": "98",
    "Zac": "154",
    "Pantheon": "80",
    "Swain": "50",
    "Bard": "432",
    "Sion": "14",
    "Vayne": "67",
    "Nasus": "75",
    "Twisted Fate": "4",
    "Cho'Gath": "31",
    "Udyr": "77",
    "Morgana": "25",
    "Volibear": "106",
    "Caitlyn": "51",
    "Darius": "122",
    "Nocturne": "56",
    "Zilean": "26",
    "Azir": "268",
    "Rumble": "68",
    "Skarner": "72",
    "Teemo": "17",
    "Urgot": "6",
    "Amumu": "32",
    "Galio": "3",
    "Heimerdinger": "74",
    "Ashe": "22",
    "Vel'Koz": "161",
    "Singed": "27",
    "Varus": "110",
    "Twitch": "29",
    "Garen": "86",
    "Diana": "131",
    "Master Yi": "11",
    "Elise": "60",
    "Alistar": "12",
    "Katarina": "55",
    "Ekko": "245",
    "Mordekaiser": "82",
    "Kog'Maw": "96",
    "Aatrox": "266",
    "Draven": "119",
    "Tahm Kench": "223",
    "Fiddlesticks": "9",
    "Talon": "91",
    "Xin Zhao": "5",
    "Lee Sin": "64",
    "Taric": "44",
    "Malzahar": "90",
    "Lissandra": "127",
    "Tristana": "18",
    "Rek'Sai": "421",
    "Vladimir": "8",
    "Jarvan IV": "59",
    "Nami": "267",
    "Soraka": "16",
    "Veigar": "45",
    "Janna": "40",
    "Nautilus": "111",
    "Evelynn": "28",
    "Gragas": "79",
    "Zed": "238",
    "Vi": "254",
    "Lulu": "117",
    "Ahri": "103",
    "Quinn": "133",
    "LeBlanc": "7",
    "Ezreal": "81",
}

class HTTPException(Exception):
    pass

class LoLAPI():

    def __init__(self, api_key='8fe8525b-d2c4-4850-a33b-d412cb959cd1', region="na", refresh=False):
        
        self.region = region
        self.api_key = api_key
        self.key_end = "?api_key=" + self.api_key
        
        self.refresh = refresh
        
        self.base_url = "https://na.api.pvp.net/api/lol/" + self.region 
        self.team_base_url = "https://na.api.pvp.net/api/lol/" + self.region + "/v2.4"
        
        self.static_url = "https://global.api.pvp.net/api/lol/static-data/" + self.region + "/v1.2/"
        
        self.champion_url = self.base_url + "/v1.2/champion/"
        self.summoner_url = self.base_url + "/v1.4/summoner/"
    
    def send_cached_req(self, cachepath, url):
        if self.refresh == False and os.path.isfile(cachepath):
            with open(cachepath, 'r') as f:
                data = json.load(f)
        else:
            data = self.send_req(url)
            with open(cachepath, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)
        return data
    
    """ STATIC INFO """
    if True:
        def get_champion_list(self, champData=[]):
            url = self.static_url + "champion" + self.key_end
            if len(champData) > 0:
                url += "&champData=" + ",".join(champData)
            
            return self.send_cached_req('json_cache/get_champion_list.json', url)

        def get_champion(self, id, champData=[]):
            cachepath = 'json_cache/%s.json' % id
            
            id = str(id)
            if not id.isdigit():
                id = champ_map[id]
            
            url = self.static_url + "champion/" + id + self.key_end
            if len(champData) > 0:
                url += "&champData=" + ",".join(champData)

            return self.send_cached_req(cachepath, url)
        
        def get_item_list(self, itemListData=[]):
            url = self.static_url + "item" + self.key_end
            if len(itemListData) > 0:
                url += '&itemListData=' + ','.join(itemListData)
            
            return self.send_cached_req('json_cache/get_item_list.json', url)
        
        def get_item(self, id, itemListData=[]):
            id = str(id)
            url = self.static_url + "item/" + id + self.key_end
            return self.send_req(url)
        
    """ SUMMONER INFO """
    if True:
        def get_summoner_by_id(self, id):
            url = self.summoner_url + str(id) + self.key_end
            return self.send_req(url)

        def get_summoners_by_id(self, ids):
            ids = map(str, ids)
            url = self.summoner_url + ",".join(ids) + "/name" + self.key_end
            return self.send_req(url)

        def get_summoner_by_name(self, name):
            url = self.summoner_url + "by-name/" + name + self.key_end
            return self.send_req(url)

        def get_rune_pages_by_id(self, id):
            url = self.summoner_url + str(id) + "/runes" + self.key_end
            return self.send_req(url)

        def get_rune_pages_by_summoner(self, summoner):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_rune_pages_by_id(summoner_id)

        def get_masteries_by_id(self, id):
            url = self.summoner_url + str(id) + "/masteries" + self.key_end
            return self.send_req(url)

        def get_masteries_by_summoner(self, summoner):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_masteries_by_id(summoner_id)

    """ TEAMS """
    if True:
        def get_teams_for_id(self, id):
            url = self.team_base_url + "/team/by-summoner/" + str(id) + self.key_end
            return self.send_req(url)

        def get_teams_for_summoner(self, summoner):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_teams_for_id(summoner_id)

    """ STATS """
    if True:
        def get_normal_stats_by_id(self, id, season=None):
            url = self.base_url + "/stats/by-summoner/" + str(id) + "/summary"
            if season == 3:
                url += "?season=SEASON3&" + self.key_end[1:]
            elif season == 4:
                url += "?season=SEASON4&" + self.key_end[1:]
            else:
                url += self.key_end
            return self.send_req(url)

        def get_normal_stats_by_summoner(self, summoner, season=None):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_normal_stats_by_id(summoner_id, season)

        def get_ranked_stats_by_id(self, id, season=None):
            url = self.base_url + "/stats/by-summoner/" + str(id) + "/ranked"
            if season == 3:
                url += "?season=SEASON3&" + self.key_end[1:]
            elif season == 4:
                url += "?season=SEASON4&" + self.key_end[1:]
            else:
                url += self.key_end
            return self.send_req(url)

        def get_ranked_stats_by_summoner(self, summoner, season=None):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_ranked_stats_by_id(summoner_id, season)

    """ LEAGUES """
    if True:
        def get_league_data_by_id(self, id):
            url = self.team_base_url + "/league/by-summoner/" + str(id) + self.key_end
            return self.send_req(url)

        def get_league_data_by_summoner(self, summoner):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_league_data_by_id(summoner_id)

    """ GAMES """
    if True:
        def get_recent_games_by_id(self, id):
            url = self.base_url + "/game/by-summoner/" + str(id) + "/recent" + self.key_end
            return self.send_req(url)

        def get_recent_games_by_summoner(self, summoner):
            json_dict = self.get_summoner_by_name(summoner)
            summoner_id = json_dict["id"]
            return self.get_recent_games_by_id(summoner_id)

    """ CHAMPIONS """
    if True:
        def get_all_champions(self):
            url = self.base_url + "/champion" + self.key_end
            return self.send_req(url)

        def get_free_champions(self):
            url = self.base_url + "/champion?freeToPlay=true&" + self.key_end[1:]
            return self.send_req(url)

    """ INTERNAL FUNCS """
    def send_req(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return self.get_status_error(r.status_code)

    def get_status_error(self, status):
        if status == 400:
            raise HTTPException("400 Error - Bad Request")
        elif status == 401:
            raise HTTPException("401 Error - Invalid URL")
        elif status == 404:
            raise HTTPException("404 Error - Summoner Not Found")
        elif status == 500:
            raise HTTPException("500 Error - Internal Server Error")
        else:
            raise HTTPException(str(status) + " Error - Unknown")
            
def main():
    # key = "8fe8525b-d2c4-4850-a33b-d412cb959cd1"
    api = LoLAPI()

    champion_data = api.get_champion_list(['stats'])
    # print champion_data
    # champion_data = champion_list["stats"]
    # print "champ_map = {"
    # for ckey in champion_data['data']:
    #     stats = champion_data['data'][ckey]['stats']
    #     if stats['critperlevel'] != 0:
    #         print stats['critperlevel']
    #     data = champion_data[ckey]
    #     print '\"' + data["name"] + "\": \"" + str(data["id"]) + "\","
    # print "}"
    
    # print api.get_item(1410)
    
    # print api.get_item_list(['effect', 'from', 'gold', 'stats'])
    # print api.get_champion('Kindred', ['stats', 'spells'])
    
if __name__ == "__main__":
    main()