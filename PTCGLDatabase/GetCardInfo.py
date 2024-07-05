from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
import requests
import os
from bs4 import BeautifulSoup
from django.db import transaction
from collections import namedtuple
import argparse
from datetime import datetime
import pymssql

connection_format = 'mssql+pymssql://{0}:{1}@{2}/{3}?charset=utf8'
connection_str = connection_format.format('sa','KUEkue520520','192.168.23.100','PTCG')
engine = create_engine(connection_str,echo=False) 


Base = declarative_base()
# 設置 SQLite 數據庫路徑
#db_path = 'sqlite:///D:/Python/PTCGL/PTCGLHelper/db.sqlite3'
# 創建 SQLAlchemy 引擎
#engine = create_engine(db_path, echo=True)  # 使用 echo=True 可以顯示 SQL 語句
# 創建 Session class，用於與數據庫交互
Session = sessionmaker(bind=engine)
# 創建 Base class，所有的 model class 將繼承自它
Base.metadata.create_all(engine)
# 創建 Session
session = Session()


class PokemonCard(Base):
    __tablename__ = 'CardInfo_pokemoncard'

    id = Column(Integer, primary_key=True)
    card_name = Column(String(30), nullable=True)
    evolve_marker = Column(String(10), nullable=True)
    card_hp = Column(String(10), nullable=True)
    Type = Column(String(10), nullable=True)
    Weakness = Column(String(10), nullable=True)
    Resistance = Column(String(10), nullable=True)
    Escape = Column(String(10), nullable=True)
    description = Column(Text, nullable=True)
    card_alpha = Column(String(10), nullable=True)
    card_rule = Column(String(20), nullable=True)
    card_number = Column(String(20), nullable=True)
    web_id = Column(String(100), nullable=True)
    web_url = Column(String(200), nullable=True)

    def __repr__(self):
        return f'<PokemonCard(card_name={self.card_name}, Type={self.Type})>'

class PokemonCardSkill(Base):
    __tablename__ = 'CardInfo_pokemoncardskill'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('CardInfo_pokemoncard.id'), nullable=False)
    card = relationship('PokemonCard', backref='skills')
    skill_type = Column(String(10), nullable=True)
    skill_name = Column(String(100), nullable=True)
    skill_cost = Column(String(100), nullable=True)
    skill_damage = Column(String(100), nullable=True)
    skill_effect = Column(String(100), nullable=True)

    def __repr__(self):
        return f'<PokemonCardSkill(skill_name={self.skill_name}, card={self.card.card_name})>'


def check_for_grass_img(imgContent):
    str_representation = str(imgContent)
    if 'Grass.png' in str_representation:
        return '草'
    elif 'Colorless.png' in str_representation:
        return '無'
    elif 'Fire.png' in str_representation:
        return '火'
    elif 'Water.png' in str_representation:
        return '水'
    elif 'Lightning.png' in str_representation:
        return '雷'
    elif 'Psychic.png' in str_representation:
        return '超'
    elif 'Fighting.png' in str_representation:
        return '鬥'
    elif 'Darkness.png' in str_representation:
        return '惡'
    elif 'Metal.png' in str_representation:
        return '鋼'
    elif 'Fairy.png' in str_representation:
        return '妖'
    elif 'Dragon.png' in str_representation:
        return '龍'
    else:
        return None
    
def crawl_PokemonCardInfo(soup,PokemonInfo):
        #h1 PTCG網站中有進化資訊與他的名字        
        h1_tag = soup.find('h1', class_='pageHeader cardDetail')
        evolve_marker = h1_tag.find('span', class_='evolveMarker').text.strip()
        pokemon_name = h1_tag.contents[-1].strip()

        # 獲取HP值
        hp_span = soup.find('span', class_='number')
        hp = hp_span.text if hp_span else 'N/A'

        # 獲取屬性
        p_tag = soup.find('p', class_='mainInfomation')
        if p_tag:
            # 找到屬性右邊的<img>元素
            img_tag = p_tag.find('img')
        type_value = check_for_grass_img(img_tag.prettify())

        # 獲取弱點、抵抗力和撤退
        weakpoint_td = soup.find('td', class_='weakpoint')
        weakpoint = check_for_grass_img(weakpoint_td.prettify()) if weakpoint_td else 'N/A'

        resist_td = soup.find('td', class_='resist')
        resist = check_for_grass_img(resist_td.prettify()) if resist_td else 'N/A'

        escape_td = soup.find('td', class_='escape')
        escapes = escape_td.find_all('img')
        #escape = check_for_grass_img(escape_td.prettify()) if escape_td else 'N/A'
        escape = ''
        for escape_img in escapes:
            result = check_for_grass_img(escape_img)
            if result:
                escape +=  result
        PokemonInfo["pokemon_name"] = pokemon_name
        PokemonInfo["evolve_marker"] = evolve_marker
        PokemonInfo["hp"] = hp
        PokemonInfo["type_value"] = type_value
        PokemonInfo["weakpoint"] = weakpoint
        PokemonInfo["resist"] = resist
        PokemonInfo["escape"] = escape
        # print(f'pokemon_name: {pokemon_name}')
        # print(f'evolve_marker: {evolve_marker}')
        # print(f'HP: {hp}')
        # print(f'Type: {type_value}')
        # print(f'Weakness: {weakpoint}')
        # print(f'Resistance: {resist}')
        # print(f'Escape: {escape}')

  
def crawl_for_skillInfo(soup,SkillInfos):
    skills_div = soup.find('div', class_='skillInformation')
    if skills_div:
        skills = skills_div.find_all('div', class_='skill')
        for skill in skills:
            skill_name = skill.find('span', class_='skillName').text.strip()
                #需要改段落
            span_tag = skill.find('span', class_='skillCost')
            costs = span_tag.find_all('img')
            skill_cost = ''
            for cost in costs:
                result = check_for_grass_img(cost)
                skill_cost = skill_cost + result 
            skill_damage = skill.find('span', class_='skillDamage').text.strip()
            skill_effect = skill.find('p', class_='skillEffect').text.strip()
                        # 創建一個空字典來存儲技能信息
            sk = {}
            sk['skill_name'] = skill_name
            sk['skill_cost'] = skill_cost
            sk['skill_damage'] = skill_damage
            sk['skill_effect'] = skill_effect
            # 將字典添加到列表中
            SkillInfos.append(sk)

def crawl_for_version(soup,PokemonInfo):
    card_version_img = str(soup.find('span', class_='expansionSymbol').find('img')['src'])
    card_alpha = soup.find('span', class_='alpha').text.strip()
    card_num = soup.find('span', class_='collectorNumber').text.strip()
    filename = os.path.basename(card_version_img).replace('.png','')

    PokemonInfo["card_version"] = filename
    PokemonInfo["card_alpha"] = card_alpha
    PokemonInfo["card_num"] = card_num

def check_web_id_exists(web_id):
    try:
        # 查詢資料庫中是否存在指定的 web_id
        card = session.query(PokemonCard).filter_by(web_id=web_id).first()
        if card:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        print(f"Error checking web_id {web_id}: {e}")
        return False


def crawl_start(url,id):

    #判斷id是否存在
    if check_web_id_exists(id):
        print(f'此寶可夢已經寫入資料庫 URL:{url}, id:{id}')
        return
    

    PokemonInfo = {}
    SkillInfos = []
    
        # 發送 GET 請求獲取網頁內容
    response = requests.get(url)
    # 檢查是否成功獲取網頁
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        h1 = soup.find('h1', class_='pageHeader').text.strip()
        if h1 == '卡牌搜尋結果':
            # 在這裡處理當h1等於'2'的情況
            return  # 或者做其他操作
        crawl_PokemonCardInfo(soup,PokemonInfo)
        crawl_for_version(soup,PokemonInfo)
        crawl_for_skillInfo(soup,SkillInfos)
      
        print(PokemonInfo)
        print(SkillInfos)

        new_card = PokemonCard(
            card_name=PokemonInfo["pokemon_name"],
            evolve_marker=PokemonInfo["evolve_marker"],
            card_hp=PokemonInfo["hp"],
            Type=PokemonInfo["type_value"],
            Weakness=PokemonInfo["weakpoint"],
            Resistance=PokemonInfo["resist"],
            Escape=PokemonInfo["escape"],
            card_alpha=PokemonInfo["card_version"],
            card_rule=PokemonInfo["card_alpha"],
            card_number=PokemonInfo["card_num"],
            web_id = id,
            web_url = url
        )
        session.add(new_card)
        session.commit()

        for skill in SkillInfos:
            # 創建新的 PokemonCardSkill，並關聯到已存在的 PokemonCard
            new_skill = PokemonCardSkill(
                skill_type = '招式',
                skill_name = skill["skill_name"],
                skill_cost = skill["skill_cost"],
                skill_damage = skill["skill_damage"],
                skill_effect = skill["skill_effect"],
                card=new_card
            )
            session.add(new_skill)
            session.commit()
    else:
        print(f'無法獲取網頁內容。錯誤代碼：{response.status_code}')


# 執行爬取網站的函數
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='抓寶可夢用')
    parser.add_argument('start', type=int, help='迴圈開頭')
    parser.add_argument('end', type=int, help='迴圈結尾')
    args = parser.parse_args()
    
    # 取得當前時間
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # 產生錯誤日誌檔案名稱，加入時間戳
    error_log_file = f'error_log_{args.start}_{args.end}_{timestamp}.txt'
    
    for i in range(args.start, args.end):
        url = f'https://asia.pokemon-card.com/tw/card-search/detail/{i}/'
        try:
            crawl_start(url,i)
        except Exception as e:
            # 紀錄錯誤訊息到日誌檔案
            with open(error_log_file, 'a') as f:
                f.write(f'Error for URL: {url}\n')
                f.write(f'Error message: {str(e)}\n')
            # 可以選擇在這裡繼續執行下一個迴圈，或者加上其他處理邏輯
            continue


