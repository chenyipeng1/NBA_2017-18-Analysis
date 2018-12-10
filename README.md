# Project Title

NBA 2017-18 Data Analysis

## Project description

This is SI507 Final project, authored by Yipeng Chen. I made a very simple back-end to front-end software to visualize and give a analysis on NBA 2017-18 team & player data during regular season.

## Data collection

https://www.basketball-reference.com/leagues/NBA_2018.html
https://www.basketball-reference.com/leagues/NBA_2018_per_game.html
There is a crawler program to get the data. We use cache so if you want to reload the data, you may need to delete json file.

## Getting Started

### Install virtualenv

I gave "requirement.txt" here, so you can use virtualenv to install that file.
```
$ pip3 install virtualenv
```

### Create virtual environment

Let's say you want to use your virtualenv as "venv". At your desired path,
```
$ virtualenv venv
```

### Activate virtual environment

```
$ source venv/bin/activate
```

(is you want to end virtual environment at any time: )
```
$ Deactivate
```

### Install required libraries

```
(venv) $ pip install -r /path/to/requirements.txt 
```

### Start program

```
(venv) $ python main.py
```

### View website

http://127.0.0.1:5000/


## Code Structure

### main.py
lanuch code
### crawler.py
python3 crawler
### db.py
database handle
### view.py
website view handle
### model.py
website data handle
### test.py
testcase

## Authors

* **Yipeng Chen** - *Initial work* - (https://github.com/chenyipeng1)

