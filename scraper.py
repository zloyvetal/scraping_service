import requests as rqst
from bs4 import BeautifulSoup as bs


def take_additional_data(url):
    web = rqst.get(url)
    soup = bs(web.content, "html.parser")
    img_link = soup.find('header').find('img')['src']

    game_description = soup.find('header').find_all('p')[1].text

    developer = soup.find('div', class_='S016-ency-panel-2020').find('span', id='game-developer-cnt').text.split(":")[-1]
    publisher = soup.find('div', class_='S016-game-info').find('span', id='game-publisher-cnt').text.split(":")[-1]
    return {
        'img_link': img_link,
        'game_description': game_description,
        'developer': developer,
        'publisher': publisher
    }


def scraper(url):
    """
    This function takes in a URL of a webpage and uses BeautifulSoup to scrape the page for video game info and returns
    it as a list of dictionaries.
    The keys of each dictionary are 'game_link', 'game_name', 'genre', 'platforms', and 'publisher'.
    The values are the data associated with each key.
     Parameters:
        url (str): https://www.gamepressure.com/games/games_release_dates.asp?CZA=6
     Return:
        list_with_all_scraping_data (list): A list of dictionaries containing the scraped video game info
    """
    web = rqst.get(url)
    soup = bs(web.content, "html.parser")
    table = soup.find('div', class_="daty-premier-2017")

    list_with_all_scraping_data = list()

    for row in table.find_all('a'):
        all_info = [element for element in row.contents if element != '\n']
        link = row['href']
        date = all_info[0].text
        *game_name, genre = all_info[1].text.split()
        game_platform = all_info[2].text
        disctiribution_channels = all_info[3].text

        source = "https://www.gamepressure.com/" + link
        take_additional_data_from_source = take_additional_data(source)

        data = {
            'game_info_link': source,
            'distribution_channel': disctiribution_channels,
            'game_name': " ".join(game_name),
            'date': date,
            'genre': genre,
            'platforms': game_platform,
            'publisher': take_additional_data_from_source['publisher'],
            'game_description': take_additional_data_from_source['game_description'],
            'img_link': take_additional_data_from_source['img_link'],
            "source": source,
            'developer': take_additional_data_from_source['developer']
        }

        list_with_all_scraping_data.append(data)

    return list_with_all_scraping_data



# list_with_game_info = [div.text for div in table.find_all('div')]
# print(list_with_game_info)
#
# list_with_game_info = [{
#     'game_name' : str(),
#     "релиз_дейт": str(),
#     "жанр": str(),
#     "platform": str(),
#     "sale_platform": str()
# }]
# print(table.text.strip())
# for row in table:
#     if row != '\n':
#         print(row.text.strip())
# def extract_data(table):
#     result = []
#     for row in table:
#         soup = BeautifulSoup(row, 'html.parser')
#         data = {}
#         data['href'] = soup.find('a', {'class': 'box'}).get('href')
#         data['Release Date'] = soup.find('div').text.strip()
#         game_name = soup.find('div', {'data-cnt': '73'}).text.strip().split(' ')[0]
#         game_genre = soup.find('div', {'data-cnt': '73'}).find('i').text.strip()
#         data['Game Name'] = game_name
#         data['Game Genre'] = game_genre
#         data['Platform'] = soup.find_all('div')[2].text.strip()
#         data['Shop'] = soup.find_all('div')[3].text.strip()
#         result.append(data)
#     return result
