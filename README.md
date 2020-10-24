# Profile scrape

## Description
A scraper for a site with profiles

## Getting started
Install the required packages:

```
pip install -r requirements.txt
```

Run the tests:

```
python -m unittest -v com/dreamlab/profile_scrape/test/test_*
```

Start the database:

```
docker-compose up -d
```

Starting the scrape:

```
python main.py scrape
```

For starting the server:

```
python main.py serve
```

The scraping and the server can run simultaneously as separate processes.
