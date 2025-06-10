import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import requests
import altair as alt




db_username=st.secrets['db_username']
db_password=st.secrets['db_password']
db_host=st.secrets['db_host']
db_port=st.secrets['db_port']
db_name=st.secrets['db_name']

item = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json"
perk = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"



def create_db_connection_string(db_username, db_password, db_host, db_port, db_name):
    connection_url = 'postgresql+psycopg2://'+ db_username + ':' + db_password + '@' + db_host + ':' + db_port +'/' + db_name
    return connection_url

@st.cache_data
def load_data():
    conn_url = create_db_connection_string(db_username, db_password, db_host, db_port, db_name)
    db_engine = create_engine(conn_url, pool_recycle=3600)
    query="""
    SELECT *
    FROM student.lol_analytics
    """
    return pd.read_sql_query(query, con=db_engine)


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

@st.cache_data
def get_items():
    item_json = requests.get(item).json()
    item_ids = json_extract(item_json, 'id')
    item_names = json_extract(item_json, 'name')
    return dict(map(lambda i, j : (int(i),j),item_ids, item_names))

@st.cache_data
def get_perks():
    perk_json = requests.get(perk).json()
    perk_ids = json_extract(perk_json, 'id')
    perk_names = json_extract(perk_json, 'name')
    return dict(map(lambda i, j : (int(i),j),perk_ids, perk_names))


item_dict = get_items()
perk_dict = get_perks()


  
item_dict = {str(k): v for k, v in item_dict.items()}
perk_dict = {str(k): v for k, v in perk_dict.items()}
    
df = load_data()




columns_to_replace = ["item0", "item1", "item2", "item3", "item4", "item5", "item6"]


df[columns_to_replace] = df[columns_to_replace].replace(item_dict)



columns_to_replace = ['primary_keystone','primary_perk_1','primary_perk_2','primary_perk_3','secondary_perk_1','secondary_perk_2','offense','flex','defense']
df[columns_to_replace] = df[columns_to_replace].replace(perk_dict)


df['game_duration'] = df['game_duration'].astype(int) / 60



player_info = {
    'Faker':{
        'name': 'Lee Sang-hyeok (이상혁)',
        'age': 28,
        'team': 'T1',
        'country of birth': 'South Korea'     
    },
    'Caps': {
        'name': 'Rasmus Borregaard Winther',
        'age': 25,
        'team': 'G2',
        'country of birth': 'Denmark'
    },
    'Palafox': {
        'name': 'Cristian Palafox',
        'age': 25,
        'team': 'Shopify Rebellion',
        'country of birth': 'United States'
    },
    'Chovy': {
        'name': 'Jeong Ji-hoon (정지훈)',
        'age': 23,
        'team': 'Gen.G',
        'country of birth': 'South Korea'
    },
    'Doinb': {
        'name': '	Kim Tae-sang (김태상)',
        'age': 28,
        'team': 'Ninjas in Pyjamas',
        'country of birth': 'South Korea'
    }
}


#change this later to work on puuid not riot id

df = df.replace({
    "riot_id": {
        "Hide on bush": "Faker",
        "G2 Caps": "Caps",
        "Palafoxy": "Palafox",
        "허거덩": "Chovy",
        "Heart": "Doinb"
    }
})


champion_id_map = {
    "Aatrox": 266,
    "Ahri": 103,
    "Akali": 84,
    "Alistar": 12,
    "Amumu": 32,
    "Anivia": 34,
    "Annie": 1,
    "Ashe": 22,
    "Aurelion Sol": 136,
    "Bard": 432,
    "Blitzcrank": 53,
    "Brand": 63,
    "Braum": 201,
    "Caitlyn": 51,
    "Camille": 164,
    "Cassiopeia": 69,
    "Chogath": 31,
    "Corki": 42,
    "Darius": 122,
    "Diana": 131,
    "Dr. Mundo": 36,
    "Draven": 119,
    "Ekko": 245,
    "Elise": 60,
    "Evelynn": 28,
    "Ezreal": 81,
    "Fiddlesticks": 9,
    "Fiora": 114,
    "Fizz": 105,
    "Galio": 3,
    "Gangplank": 41,
    "Garen": 86,
    "Gnar": 150,
    "Gragas": 79,
    "Graves": 104,
    "Hecarim": 120,
    "Heimerdinger": 74,
    "Illaoi": 420,
    "Irelia": 39,
    "Janna": 40,
    "Jarvan IV": 59,
    "Jhin": 202,
    "Jinx": 222,
    "Kaisa": 145,
    "Kalista": 429,
    "Karma": 43,
    "Karthus": 30,
    "Kassadin": 38,
    "Katarina": 55,
    "Kayle": 10,
    "Kennen": 85,
    "Kha'Zix": 121,
    "Kindred": 203,
    "Kled": 240,
    "Kog'Maw": 96,
    "LeBlanc": 7,
    "Lee Sin": 64,
    "Leona": 89,
    "Lillia": 876,
    "Lux": 99,
    "Malphite": 54,
    "Malzahar": 90,
    "Maokai": 57,
    "Miss Fortune": 21,
    "Nami": 117,
    "Nasus": 75,
    "Nautilus": 111,
    "Neeko": 518,
    "Olaf": 2,
    "Orianna": 61,
    "Pantheon": 80,
    "Poppy": 78,
    "Pyke": 555,
    "Qiyana": 133,
    "Rakan": 497,
    "Rammus": 33,
    "Rek'Sai": 421,
    "Renekton": 58,
    "Rengar": 107,
    "Riven": 92,
    "Rumble": 68,
    "Ryze": 13,
    "Sejuani": 113,
    "Senna": 235,
    "Shaco": 35,
    "Shen": 98,
    "Sivir": 15,
    "Sona": 37,
    "Soraka": 16,
    "Swain": 50,
    "Sylas": 517,
    "Syndra": 134,
    "Tahm Kench": 223,
    "Taliyah": 163,
    "Taric": 44,
    "Teemo": 17,
    "Thresh": 412,
    "Tristana": 18,
    "Trundle": 48,
    "Tryndamere": 23,
    "Twisted Fate": 4,
    "Udyr": 77,
    "Urgot": 6,
    "Varus": 110,
    "Vayne": 67,
    "Veigar": 45,
    "Vi": 254,
    "Viktor": 112,
    "Vladimir": 8,
    "Volibear": 106,
    "Warwick": 19,
    "Wukong": 62,
    "Xayah": 498,
    "Xerath": 101,
    "Yuumi": 350,
    "Zac": 154,
    "Zed": 238,
    "Ziggs": 115,
    "Zilean": 26,
    "Zoe": 142,
    "Zyra": 143,
    "Viego": 234, 
    "Smolder": 901,
    'Ambessa': 799,
    'Aurora': 893,
    'Yone': 777,
    'Hwei': 910,
    'Seraphine': 147,
    'Sett': 875,   
    'Lulu': 117,
    'Nocturne': 56,
    'Gwen': 887,
    'Jayce': 126
}

    
def get_champion_icon_url(champion_name):
    champion_id = champion_id_map.get(champion_name)
    
    if champion_id:
        return f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{champion_id}.png"
    else:
        return None



def render_table_with_images(df):
    html = "<table style='width:100%; border:1px solid black;'>"

    # Add table headers
    html += "<thead><tr>"
    html += "<th style='padding: 8px;'> Champion Icon </th>"  # Add title for the image column
    for column in df.columns:
        html += f"<th style='padding: 8px; text-align: left;'> {column} </th>"
    html += "</tr></thead>"

    # Add table rows with images
    html += "<tbody>"
    for index, row in df.iterrows():
        html += "<tr>"

        # Image column
        image_url = get_champion_icon_url(row['champ_name'])
        if image_url:
            html += f"<td style='padding: 8px;'><img src='{image_url}' alt='Image' style='width: 40px; height: 40px;'></td>"
        else:
            html += f"<td style='padding: 8px;'><img src='https://via.placeholder.com/40' alt='Image' style='width: 40px; height: 40px;'></td>"

        # Other columns
        for col in df.columns:
            html += f"<td style='padding: 8px;'> {row[col]} </td>"

        html += "</tr>"
    html += "</tbody></table>"

    return html
    


# df = df.replace("Hide on bush", "Faker")
# df = df.replace("G2 Caps", "Caps")
# df = df.replace("Palafoxy", "Palafox")
# df = df.replace("허거덩", "Chovy")
# df = df.replace("Heart", "Doinb")

stats = (
    df.groupby(['riot_id', 'champ_name'])
    .agg(
        pick_rate=('champ_name', 'count'), 
        wins=('win', lambda x: (x == True).sum()),  
        loses=('win', lambda x: (x == False).sum()),
        kills = ('kills', 'sum'),
        assists = ('assists', 'sum'),
        deaths = ('deaths', 'sum'),
        total_cs=('cs', 'sum'),
        total_game_duration=('game_duration', 'sum'),
    )
    .reset_index()  
)

stats['win_rate'] = (stats['wins'] / stats['pick_rate']) * 100
stats['KDA'] = (stats['kills'] + stats['assists']) / stats['deaths']
stats['CS/M'] = stats['total_cs'] / stats['total_game_duration']



tab1, tab2 = st.tabs(['Player information', 'Champion information'])

with tab1:

    player = st.selectbox("Choose a player", ("Faker", "Chovy", "Doinb", "Caps", "Palafox"))
    
    filtered_stats = (stats[stats['riot_id'] == player].sort_values(by='pick_rate', ascending=False).drop(columns=['riot_id', 'total_cs', 'total_game_duration']).reset_index(drop=True))

    order = st.selectbox('Choose how to order the table', ('pick_rate', 'wins', 'loses', 'kills', 'assists', 'deaths', 'win_rate', 'KDA', 'CS/M'))
    
    st.markdown(
        render_table_with_images(filtered_stats.sort_values(by=order, ascending=False)),
        unsafe_allow_html=True
    )

    st.write(f"Total games played: {filtered_stats['pick_rate'].sum()}")



    player_champion = st.selectbox("Choose a champion", tuple(df['champ_name'].drop_duplicates().tolist()))

    st.write(stats[stats['champ_name'] == player_champion])
    
    st.header(f"Players win rate on {player_champion}")
    st.bar_chart(data=stats[stats['champ_name'] == player_champion], x='riot_id', y='win_rate')
    
    
    champ_data = df[df['champ_name'] == player_champion]
    champ_data['total_damage_dealt'] = pd.to_numeric(champ_data['total_damage_dealt'])
    champ_data = champ_data.dropna(subset=['total_damage_dealt'])
    average_damage = champ_data.groupby('riot_id', as_index=False)['total_damage_dealt'].mean()
    champ_data['damage_per_minute'] = champ_data['total_damage_dealt'] / champ_data['game_duration']
    average_damage_pm = champ_data.groupby('riot_id', as_index=False)['damage_per_minute'].mean()
    
    
    chart = alt.Chart(average_damage).mark_bar().encode(
    x=alt.X('riot_id', title='Player'),
    y=alt.Y('total_damage_dealt', title='Average Damage Dealt Per Game')
    ).properties(
    title='Average Damage Dealt Per Game for Each Player'
    )
    
    chart1 = alt.Chart(average_damage_pm).mark_bar().encode(
    x=alt.X('riot_id', title='Player'),
    y=alt.Y('damage_per_minute', title='Average Damage Dealt Per Minute')
    ).properties(
    title='Average Damage Dealt Per Minute for Each Player'
    )
    

    
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.altair_chart(chart1, use_container_width=True)
    

    columns = ['champ_level','win','game_duration', 'kills', 'assists', 'deaths', 'cs', 'gold_earned', 'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'primary_keystone', 'primary_perk_1', 'primary_perk_2', 'primary_perk_3', 'secondary_perk_1','secondary_perk_2', 'offense', 'flex', 'defense', 'total_damage_dealt']

    with st.expander("Caps"):
        filtered_champ_caps = df[(df['riot_id'] == 'Caps') & (df['champ_name'] == player_champion)]
        st.write(filtered_champ_caps[columns])
        
    with st.expander("Chovy"):
        filtered_champ_chovy = df[(df['riot_id'] == 'Chovy') & (df['champ_name'] == player_champion)]
        st.write(filtered_champ_chovy[columns])
        
    with st.expander("Faker"):
        filtered_champ_faker = df[(df['riot_id'] == 'Faker') & (df['champ_name'] == player_champion)]
        st.write(filtered_champ_faker[columns])
        
    with st.expander("Palafox"):
        filtered_champ_palafox = df[(df['riot_id'] == 'Palafox') & (df['champ_name'] == player_champion)]
        st.write(filtered_champ_palafox[columns])
        
    with st.expander("Doinb"):
        filtered_champ_doinb = df[(df['riot_id'] == 'Doinb') & (df['champ_name'] == player_champion)]
        st.write(filtered_champ_doinb[columns])
        
    


with tab2:
    champion = st.selectbox("Choose a champion", tuple(df[df['riot_id'] == player]['champ_name'].drop_duplicates().tolist()))
    st.image(get_champion_icon_url(champion))
    st.write(df[df['champ_name'] == champion].drop(columns=['uuid']))
    st.write(f"Win rate: {df[df['champ_name'] == champion]['win'].mean()*100}")
    item_columns = ["item0", "item1","item2","item3", "item4","item5"]
    all_items = df[df['champ_name'] == champion][item_columns].values.flatten()
    item_counts = pd.Series(all_items).value_counts()
    
    item_percentages = (item_counts/len(df[df['champ_name'] == champion])) * 100

    results = pd.DataFrame({
        "Amount purchased": item_counts,
        "Percentage of Games %": item_percentages
    })
    show = False
    #col1, col2 = st.columns(2)
    #with col1:
    st.write("Common Items")
    st.write(results)
    #with col2:
          # Filter results for a specific champion

        # Create multiselect widget
    selected_items = st.multiselect("Select items:", options=results.head(10).iterrows())

    if selected_items:
        # Filter rows where all selected items are present in any item column
        item_columns = ['item0', 'item1', 'item2', 'item3', 'item4', 'item5']
        filtered_df = df[df['champ_name'] == champion]  # Filter by champion
        for item in selected_items:
            filtered_df = filtered_df[filtered_df[item_columns].isin([item]).any(axis=1)]

        st.write(filtered_df)
    else:
        st.write("Select items to filter the data.")
                
        

with st.sidebar:
    
    st.header(player)
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Name: {player_info[player]['name']}")
        st.write(f"Age: {player_info[player]['age']}")
        st.write(f"Team: {player_info[player]['team']}")
        st.write(f"Country of Birth: {player_info[player]['country of birth']}")
    with col2:
        st.image(f"./images/{player}.png")
    
    
    st.write("Most played champions")
    
    
    
    st.markdown(
        render_table_with_images(filtered_stats.drop(columns=['wins', 'loses', 'kills', 'assists', 'deaths']).head(5)),
        unsafe_allow_html=True
    )
    
    
    

    