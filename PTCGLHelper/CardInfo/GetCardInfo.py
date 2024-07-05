import requests
import os
from bs4 import BeautifulSoup
from django.db import transaction
from models import PokemonCard
from collections import namedtuple


def Startcrawl():
    url = 'https://asia.pokemon-card.com/tw/card-search/detail/10618/'  # 替換成你想爬取的網站 URL
    crawl_website(url)

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
    
def crawl_website(url):
    # 發送 GET 請求獲取網頁內容
    response = requests.get(url)
    # 檢查是否成功獲取網頁
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        PokemonInfo = namedtuple('PokemonInfo', ['pokemon_name', 'evolve_marker', 'hp', 'type_value', 'weakpoint', 'resist', 'escape'])
        PokemonInfo.pokemon_name = 'a'
        print(PokemonInfo.pokemon_name)
        
        #crawl_PokemonCardInfo(soup)
        #crawl_for_skillInfo(soup)
        #crawl_for_version(soup)
    else:
        print(f'無法獲取網頁內容。錯誤代碼：{response.status_code}')
    
def create_pokemon_card_with_skills():
    try:
        with transaction.atomic():
            # 創建 PokemonCard 物件但不保存到資料庫
            new_card = PokemonCard.objects.create(
                card_name='皮卡丘',
            )
            
            # 創建多個 PokemonCardSkill 物件並關聯到剛剛創建的卡片
            skills_data = [
                {'skill_name': '電擊'},
                {'skill_name': '十萬伏特'},
                {'skill_name': '電磁波'}
            ]
            for skill_data in skills_data:
                PokemonCardSkill.objects.create(
                    card=new_card,
                    skill_name=skill_data['skill_name']
                )
            
            # 如果所有操作都成功，提交事務
            transaction.commit()
    except Exception as e:
        # 如果出現錯誤，回滾事務
        transaction.rollback()
        print(f"Error occurred: {str(e)}")


def crawl_PokemonCardInfo(soup):
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

        print(f'pokemon_name: {pokemon_name}')
        print(f'evolve_marker: {evolve_marker}')
        print(f'HP: {hp}')
        print(f'Type: {type_value}')
        print(f'Weakness: {weakpoint}')
        print(f'Resistance: {resist}')
        print(f'Escape: {escape}')

  
def crawl_for_skillInfo(soup):
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

    print('---')
    print(f'Skill: {skill_name}')
    print(f'Cost: {skill_cost}')
    print(f'Damage: {skill_damage}')
    print(f'Effect: {skill_effect}')
    print('---')   

def crawl_for_version(soup):
    card_version_img = str(soup.find('span', class_='expansionSymbol').find('img')['src'])
    card_alpha = soup.find('span', class_='alpha').text.strip()
    card_num = soup.find('span', class_='collectorNumber').text.strip()
    filename = os.path.basename(card_version_img).replace('.png','')
    print(f'Skill: {filename}')
    print(f'Cost: {card_alpha}')
    print(f'Damage: {card_num}')
    


# 執行爬取網站的函數
if __name__ == '__main__':
    url = 'https://asia.pokemon-card.com/tw/card-search/detail/10618/'  # 替換成你想爬取的網站 URL
    crawl_website(url)