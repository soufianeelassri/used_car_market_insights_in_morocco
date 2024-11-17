from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_links(page_index):
    list_of_links = []
    url = f'https://www.wandaloo.com/occasion/?marque=0&modele=0&budget=0&categorie=0&moteur=0&transmission=0&equipement=-&ville=0&vendeur=0&abonne=0&za&pg={page_index}'
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        li_tags = soup.find_all('li', class_=['odd', 'even'])
        print(li_tags)
        for li in li_tags:
            a_tag = li.find('a', class_='img')
            list_of_links.append(a_tag['href'])
        return list_of_links
    
    except requests.exceptions.RequestException as e:
        print(f'Error fetching links from page {page_index}: {e}')
        return []
    
def save_links():
    data = {'links': []}
    
    for i in range(1, 256):
        print(f'fetching links from page {i}')
        links = get_links(i)
        if links:
            data['links'].extend(links)
        else:
            print(f'No links fetched from page {i}')
            
    df = pd.DataFrame(data, columns=['links'])
    df.to_csv('../data/links.csv', index=False, header=True)
    
save_links()