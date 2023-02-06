# Scraping service


## Getting Started

### Prerequisites

* [Python 3.9.16](https://www.python.org/downloads/release/python-3916/)
* [PostgresSQL version 15](https://www.postgresql.org/download/)

### Installing

* Clone the git repository:

```
git clone https://github.com/zloyvetal/scraping_service.git
cd scraping_service
```

* Install the dependencies:

```
pip3 install -r requirements.txt
```


### Running

```
# python3 main.py
if u neeed to drop db and create new one:
# python3 redb.py
# python main.py
```

### Testing

* test.http contain three get examples
* http://localhost:8000/docs has info about api and validation
* open games_2023.csv - this is result of parsing url - "https://www.gamepressure.com/games/games_release_dates.asp?CZA=6"
