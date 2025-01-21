from dotenv import load_dotenv
import os
import requests
import pandas as pd
from pangres import upsert
from sqlalchemy import text, create_engine
import time
load_dotenv()

api_key = os.environ.get('riot_api_key')

db_username=os.environ.get('db_username')
db_password=os.environ.get('db_password')
db_host=os.environ.get('db_host')
db_port=os.environ.get('db_port')
db_name=os.environ.get('db_name')



def get_puuid(summonerId=None, gameName=None, tagLine=None, region="europe"):
    
    if summonerId is not None:
        root_url = f"https://{region}.api.riotgames.com/"
        endpoint = 'lol/summoner/v4/summoners/'
        response = requests.get(root_url+endpoint+summonerId+"?api_key="+api_key)
        
        return response.json()['puuid']
    else:
        root_url = f"https://{region}.api.riotgames.com/"
        endpoint = f'riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'
        response = requests.get(root_url+endpoint+"?api_key="+api_key)
        return response.json()['puuid']
    

def get_idtag_from_puuid(puuid=None):
    root_url="https://europe.api.riotgames.com/"
    endpoint="/riot/account/v1/accounts/by-puuid/"
    
    response = requests.get(root_url+endpoint+puuid+"?api_key="+api_key)
    
    id = {
        'gameName': response.json()['gameName'],
        'tagLine': response.json()['tagLine']
    }
    
    return id
       
    
def get_match_history(region=None, puuid=None, start=0, count=20):
    root_url = f"https://{region}.api.riotgames.com/"
    endpoint = f'lol/match/v5/matches/by-puuid/{puuid}/ids'
    query_params = f'?start={start}&count={count}'
    response = requests.get(root_url+endpoint+query_params+'&api_key='+api_key)
    return response.json()

def get_match_data_from_id(region=None, matchId=None):
    root_url = f"https://{region}.api.riotgames.com/"
    endpoint = f'lol/match/v5/matches/{matchId}'
    
    while True:
        
        response = requests.get(root_url+endpoint+'?api_key='+api_key)
        if response.status_code == 429:
            time.sleep(10)
            continue
    
        return response.json()

def process_match_json(match_json, puuid):
    metadata=game['metadata']
    info = game['info']
    players= info['participants']





    match_id = metadata['matchId']
    participants = metadata['participants']
    teams = info['teams']
    player = players[participants.index(puuid)]

    game_creation = info['gameCreation']
    game_duration = info['gameDuration']
    

    assists = player['assists']
    champ__level = player['champLevel']
    
    champ_name = player['championName']
    
    deaths = player['deaths']
    
    gold_earned = player['goldEarned']
    item0 = player['item0']
    item1 = player['item1']
    item2 = player['item2']
    item3 = player['item3']
    item4 = player['item4']
    item5 = player['item5']
    item6 = player['item6']
    kills = player['kills']
    
    riot_id = player['riotIdGameName']
    
    total_damage_dealt = player['totalDamageDealtToChampions']
    
    total_minions_killed = player['totalMinionsKilled']
    
    win = player['win']


    

    perks = player['perks']
    stats = perks['statPerks']
    styles = perks['styles']

    primary = styles[0]
    secondary = styles[1]

    defense = stats['defense']
    flex = stats['flex']
    offense = stats['offense']

    

    primary_keystone = primary['selections'][0]['perk']
    primary_perk_1 = primary['selections'][1]['perk']
    primary_perk_2 = primary['selections'][2]['perk']
    primary_perk_3 = primary['selections'][3]['perk']


    secondary_perk_1 = secondary['selections'][0]['perk']
    secondary_perk_2 = secondary['selections'][1]['perk']
    


    matchDF = pd.DataFrame({
        
        'riot_id': [riot_id],
        'champ_name': [champ_name],
        'champ_level': [champ__level],
        'win':[win],
        'game_duration':[game_duration],
        'gold_earned':[gold_earned],
        'game_creation': [game_creation],
        'kills': [kills],
        'assists': [assists],
        'deaths': [deaths],
        'item0': [item0],
        'item1': [item1],
        'item2': [item2],
        'item3': [item3],
        'item4': [item4],
        'item5': [item5],
        'item6': [item6],
        'cs':[total_minions_killed],
        'total_damage_dealt': [total_damage_dealt],
        'primary_keystone': [primary_keystone],
        'primary_perk_1': [primary_perk_1],
        'primary_perk_2': [primary_perk_2],
        'primary_perk_3': [primary_perk_3],
        'secondary_perk_1':[secondary_perk_1],
        'secondary_perk_2':[secondary_perk_2],
        'offense':[offense],
        'flex':[flex],
        'defense':[defense],
        'puuid': [puuid],
        'match_id': [match_id]
    })
    return matchDF


match_ids = get_match_history(region="asia", puuid="qOK6JG8vkCv-JwMF_ynePiFTUkwnrAyw2CmeTs2HRfiEdv43bOu5-Bu9ir4GLgQTXvA6fha_Ny5LeQ")

df = pd.DataFrame()
for match_id in match_ids:
    game = get_match_data_from_id(region="asia", matchId=match_id)
    matchDF = process_match_json(game,puuid="qOK6JG8vkCv-JwMF_ynePiFTUkwnrAyw2CmeTs2HRfiEdv43bOu5-Bu9ir4GLgQTXvA6fha_Ny5LeQ")
    
    df = pd.concat([df, matchDF])
    
match_ids1 = get_match_history(region="europe", puuid="Hpexe8o8tsweiRx5QrxtDYZcL1Wf09myUmGRIq8GsFz57lmYfUDHtEDFApaZm6yFtdiTO0u2SIYPMg")

df1 = pd.DataFrame()
for match_id in match_ids1:
    game = get_match_data_from_id(region="europe", matchId=match_id)
    matchDF = process_match_json(game,puuid="Hpexe8o8tsweiRx5QrxtDYZcL1Wf09myUmGRIq8GsFz57lmYfUDHtEDFApaZm6yFtdiTO0u2SIYPMg")
    
    df1 = pd.concat([df1, matchDF])
    
match_ids2 = get_match_history(region="americas", puuid="U55Ywv-o2y3CNAEjwAb1W71ZkRq1TnBo7besicUHLEzMZcDmhPqGXeL7yJCpsgBO418wxTOxaO0OSw")

df2 = pd.DataFrame()
for match_id in match_ids2:
    game = get_match_data_from_id(region="americas", matchId=match_id)
    matchDF = process_match_json(game,puuid="U55Ywv-o2y3CNAEjwAb1W71ZkRq1TnBo7besicUHLEzMZcDmhPqGXeL7yJCpsgBO418wxTOxaO0OSw")
    
    df2 = pd.concat([df2, matchDF])
    
match_ids3 = get_match_history(region="asia", puuid="kzCRHhIeO4ROx2VCTp25bng10S1eOu_woS7ouTXHZTFUnV2EwePIgnCAMgoHh_i3ujLr2mOIhuGfTQ")

df3 = pd.DataFrame()
for match_id in match_ids3:
    game = get_match_data_from_id(region="asia", matchId=match_id)
    matchDF = process_match_json(game,puuid="kzCRHhIeO4ROx2VCTp25bng10S1eOu_woS7ouTXHZTFUnV2EwePIgnCAMgoHh_i3ujLr2mOIhuGfTQ")
    
    df3 = pd.concat([df3, matchDF])
    
match_ids4 = get_match_history(region="asia", puuid="yFNithQrfckTouEK2EQGXkuiPlh_-fWw5394QjckkJr95NKlDXJafMHaPbPbLOniInKCXtElsvzh8w")

df4 = pd.DataFrame()
for match_id in match_ids4:
    game = get_match_data_from_id(region="asia", matchId=match_id)
    matchDF = process_match_json(game,puuid="yFNithQrfckTouEK2EQGXkuiPlh_-fWw5394QjckkJr95NKlDXJafMHaPbPbLOniInKCXtElsvzh8w")
    
    df4 = pd.concat([df4, matchDF])
    
df = pd.concat([df,df1,df2,df3,df4],ignore_index=True)
    
    
item = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
perk = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"
perk_style = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json"

item_json = requests.get(item).json()
perk_json = requests.get(perk).json()
perk_style_json = requests.get(perk_style).json()

def json_extract(obj, key):
    
    arr=[]
    
    def extract(obj, arr, key):
        if isinstance(obj,dict):
            for k, v in obj.items():
                if k == key:
                    arr.append(v)
                elif isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
                
        return arr
    values = extract(obj, arr, key)
    return values

item_ids = json_extract(item_json, 'id')
item_names = json_extract(item_json, 'name')

perk_ids = json_extract(perk_json, 'id')
perk_names = json_extract(perk_json, 'name')

perk_style_ids = json_extract(perk_style_json, 'id')
perk_style_names = json_extract(perk_style_json, 'name')

item_dict = dict(map(lambda i, j : (int(i),j),item_ids, item_names))
perk_dict = dict(map(lambda i, j : (int(i),j),perk_ids, perk_names))
perk_style_dict = dict(map(lambda i, j : (int(i),j),perk_style_ids, perk_style_names))


# print(df)
# df= df[['item0','item1','item2','item3','item4','item5','item6']].replace(item_dict)
# df = df[['primary_keystone', 'primary_perk_1','primary_perk_2','primary_perk_3','secondary_perk_1','secondary_perk_2','offense','flex','defense']].replace(perk_dict)



def create_db_connection_string(db_username, db_password, db_host, db_port, db_name):
    connection_url = 'postgresql+psycopg2://'+ db_username + ':' + db_password + '@' + db_host + ':' + db_port +'/' + db_name
    return connection_url

conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)
db_engine = create_engine(conn_url, pool_recycle=3600)

connection = db_engine.connect()

df['uuid'] = df['match_id'] + '_' + df['puuid']
df = df.set_index('uuid')
upsert(con=connection, df=df, schema='student', table_name='lol_analytics', create_table=True, create_schema=True, if_row_exists='update')
connection.commit()