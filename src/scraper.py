from logging import getLogger

from requests import Session
from bs4 import BeautifulSoup as bs
from pydantic import ValidationError

from schemas import GameInfoSchema

log = getLogger(__name__)


session = Session()


def take_additional_data(url) -> dict[str, str]:
    web = session.get(url)
    soup = bs(web.content, "html.parser")
    info_url = soup.find('header').find('img')['src']

    game_description = soup.find('header').find_all('p')[1].text

    ency_pane = soup.find('div', class_='S016-ency-panel-2020')
    publisher = "no data"
    if ency_pane:
        publisher_cnt = ency_pane.find('span', id='game-publisher-cnt')
        if publisher_cnt:
            publisher = publisher_cnt.text.split(":")[-1]

    return {
        'info_url': info_url,
        'description': game_description,
        'publisher': publisher.strip()
    }


def scrape(url) -> list[GameInfoSchema]:
    web = session.get(url)
    soup = bs(web.content, "html.parser")
    table = soup.find('div', class_="daty-premier-2017")

    res: list[GameInfoSchema] = []
    raw: list[dict] = []
    for row in table.find_all('a'):
        all_info = [element for element in row.contents if element != '\n']
        link = row['href']
        scheduled = all_info[0].text
        *game_name, genre = all_info[1].text.split()
        game_platform = all_info[2].text.split(",").strip()
        disctiribution_channels = all_info[3].text.split(",")

        source = "https://www.gamepressure.com/" + link
        take_additional_data_from_source = take_additional_data(source)

        raw.append(dict(
            name=" ".join(game_name),
            publisher=take_additional_data_from_source['publisher'],
            scheduled=scheduled,
            platforms=game_platform,
            genre=genre,
            description=take_additional_data_from_source['description'],
            info_url=take_additional_data_from_source['info_url'],
            source_url=source,
            distribution_channels=disctiribution_channels,
        ))

    for i in raw:
        try:
            res.append(GameInfoSchema.parse_obj(i))
        except ValidationError as exc:
            log.warning(exc)
            continue

    return res
